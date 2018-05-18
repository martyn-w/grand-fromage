#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Martyn Whitwell'
__email__ = 'martyn.whitwell()gmail.com'
__version__ = '0.2.0'


import sys
import time
import os
from gps3.agps3threaded import AGPS3mechanism
from gps3 import agps3
import paho.mqtt.publish
import json
from datetime import datetime, timedelta
import geopy.distance
from apscheduler.schedulers.background import BackgroundScheduler
import pyownet
import Adafruit_BMP.BMP085 as BMP085

# local classes
from report import Report
import settings

class Tracker:
    TOPIC_SENSORS_VALUES = "{}/{}/{}".format(settings.MOSQUITTO_BASE_NAME, "sensors", "values")
    TOPIC_TRACKER_CHANGE = "{}/{}/{}".format(settings.MOSQUITTO_BASE_NAME, "tracker", "change")
    TOPIC_TRACKER_PING = "{}/{}/{}".format(settings.MOSQUITTO_BASE_NAME, "tracker", "ping")

    def __init__(self):
        self.gps_socket = agps3.GPSDSocket()
        self.data_stream = agps3.DataStream()
        self.gps_socket.connect(settings.GPSD_SERVER)
        self.gps_socket.watch()

        self.owproxy = pyownet.protocol.proxy(host=settings.OW_SERVER, port=4304, flags=0, persistent=False, verbose=False)
        self.bmp180 = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
        self.previous_position = None
        self.last_ping = None

    def significant_change(self, latest_position):
        if (self.previous_position is None and latest_position is not None):
            return True
        elif (self.previous_position is not None and latest_position is not None):
            delta = geopy.distance.vincenty(self.previous_position, latest_position).meters
            return delta > settings.TRACKER_SIGNIFICANT_DISTANCE_METERS
        else:
            return False

    def significant_ping(self):
        if settings.TRACKER_PING_FREQUENCY <= 0:
            # if pings have been disabled, just return
            return False
        elif self.last_ping is None:
            # this is the first ping
            return True
        else:
            return self.last_ping + timedelta(0,settings.TRACKER_PING_FREQUENCY) < datetime.utcnow()

    def report_sensors(self):
        data =  {}
        for sensor in self.owproxy.dir():
            try:
                id = self.owproxy.read(sensor + 'id')
                type = self.owproxy.read(sensor + 'type')
                temp_s = self.owproxy.read(sensor + 'temperature')
                temp_f = float(temp_s)
                print "%s (%s): %.3f *C" % (id, type, temp_f)
                data[id] = {'type': type, 'temp': temp_f}
            except ValueError:
                print "Could not convert value '%s' to a float" % (temp_s)
            except:
                print "Unexpected error:", sys.exc_info()[0]

        if self.bmp180:
            try:
                id = 'BMP180'
                type = 'BMP180'
                temp_f = self.bmp180.read_temperature()
                pres_l = self.bmp180.read_pressure()
                alt_f = self.bmp180.read_altitude() # take this value with a pinch of salt; it is more useful for determining changes in altitude
                print "%s: %.3f *C, %s Pa, %.1f m" % (id, temp_f, pres_l, alt_f)
                data[id] = {'type': type, 'temp': temp_f, 'pres': pres_l, 'alt': alt_f}
            except:
                print "Unexpected error:", sys.exc_info()[0]

        if data:
            data['utc'] = datetime.utcnow().isoformat()
            paho.mqtt.publish.single(self.TOPIC_SENSORS_VALUES, json.dumps(data), hostname=settings.MOSQUITTO_SERVER)

    def run(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.report_sensors, 'interval', seconds=settings.SENSOR_READ_FREQUENCY)
        scheduler.start()

        try:
            for data in self.gps_socket:
                if data:
                    report = Report(data)
                    if report.is_tpv_fix:
                        # note: to prevent significant changes from not being identified if the change between two recent
                        # measurements is less than the threshold, we should only set the previous_position WHEN a significant change is
                        # identified, i.e. NOT on every report
                        if self.significant_change(report.lat_lon):
                            print("Significant change: ", report.lat_lon)
                            paho.mqtt.publish.single(self.TOPIC_TRACKER_CHANGE, report.json_data, hostname=settings.MOSQUITTO_SERVER)
                            self.previous_position = report.lat_lon

                        if self.significant_ping():
                            print("Significant ping: ", report.lat_lon)
                            paho.mqtt.publish.single(self.TOPIC_TRACKER_PING, report.json_data, hostname=settings.MOSQUITTO_SERVER)
                            self.last_ping = datetime.utcnow()
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()
            print "Shutting down"


def main():
    """main program - draw and display time and date"""
    tracker = Tracker()
    tracker.run()


# main
if "__main__" == __name__:
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
