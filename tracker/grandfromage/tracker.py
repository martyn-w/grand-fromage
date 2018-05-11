#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Martyn Whitwell'
__email__ = 'martyn.whitwell()gmail.com'
__version__ = '0.2.0'


import sys
import time
from gps3.agps3threaded import AGPS3mechanism
from gps3 import agps3
import paho.mqtt.publish
import json
import datetime
import geopy.distance


# local classes
from report import Report
import settings

class Tracker:

    FULL_TOPIC = "{}/{}/{}".format(settings.NAME, settings.BASE_TOPIC, "tracker")
    FULL_TOPIC_CHANGE = "{}/{}".format(FULL_TOPIC, "change")
    FULL_TOPIC_PING = "{}/{}".format(FULL_TOPIC, "ping")

    def __init__(self):
        self.gps_socket = agps3.GPSDSocket()
        self.data_stream = agps3.DataStream()
        self.gps_socket.connect(settings.GPSD_SERVER)
        self.gps_socket.watch()

        self.previous_position = None
        self.latest_position = None
        self.last_ping = None

    def significant_change(self):
        if (self.previous_position is None and self.latest_position is not None):
            return True
        elif (self.previous_position is not None and self.latest_position is not None):
            delta = geopy.distance.vincenty(self.previous_position.lat_lon(), self.latest_position.lat_lon()).meters
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
            return self.last_ping + datetime.timedelta(0,settings.TRACKER_PING_FREQUENCY) < datetime.datetime.now()
    #
    def process(self, data):
        report = Report(data)
        if report.is_tpv_fix:
            self.latest_position = report
            # note: to prevent significant changes from not being identified if the change between two recent
            # measurements is less than the threshold, we should only set the previous_position WHEN a significant change is
            # identified, i.e. NOT on every report
            if self.significant_change():
                print("Significant change: ", self.latest_position.lat_lon())
                paho.mqtt.publish.single(self.FULL_TOPIC_CHANGE, self.latest_position.json(), hostname=settings.MOSQUITTO_SERVER)
                self.previous_position = self.latest_position

            if self.significant_ping():
                print("Significant ping: ", self.latest_position.lat_lon())
                paho.mqtt.publish.single(self.FULL_TOPIC_PING, self.latest_position.json(), hostname=settings.MOSQUITTO_SERVER)
                self.last_ping = datetime.datetime.now()

    def run(self):
        for data in self.gps_socket:
            if data:
                self.process(data)
            time.sleep(1.0)




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
