#!/usr/bin/env python

# Based on https://github.com/PiSupply/PaPiRus/blob/master/bin/papirus-clock

# Copyright 2013-2015 Pervasive Displays, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

from __future__ import print_function

import os
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from papirus import Papirus
from papirus import LM75B
import paho.mqtt.client as mqtt



# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print("Please run script as root")
        sys.exit()




class Display:
    WHITE = 1
    BLACK = 0

    BOLD_FONT_FILE = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
    PLAIN_FONT_FILE  = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'
    MESSAGE_BROKER = 'mosquitto'


    def __init__(self, rotation):
        self.papirus = Papirus(rotation=rotation)

        print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=self.papirus.panel, w=self.papirus.width,
                                                                                       h=self.papirus.height,
                                                                                       v=self.papirus.version, g=self.papirus.cog,
                                                                                       f=self.papirus.film))
        self.papirus.clear()

        # initially set all white background
        self.image = Image.new('1', self.papirus.size, self.WHITE)

        # prepare for drawing
        self.draw = ImageDraw.Draw(self.image)
        self.width, self.height = self.image.size

        self.sensor = LM75B()

        self.clock_font = ImageFont.truetype(self.BOLD_FONT_FILE, 15)
        self.date_font = ImageFont.truetype(self.PLAIN_FONT_FILE, 15)
        self.temp_font = ImageFont.truetype(self.BOLD_FONT_FILE, 15)




        # clear the display buffer
        self.clear_display_buffer()


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")


    def on_message(self, client, userdata, message):
        print(message.topic + " " + str(message.payload))



    def run(self):
        previous_second = 0
        previous_minute = 0
        previous_day = 0
        previous_tempC = ''

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.MESSAGE_BROKER)

        self.clear_display_buffer()


        while True:
            while True:
                now = datetime.today()
                client.loop()
                if now.second != previous_second:
                    break
                time.sleep(0.5)

            self.draw_clock(now)

            tempC = self.get_temp()
            if tempC != previous_tempC:
                self.draw_temp(tempC)
                previous_tempC = tempC

            if now.day != previous_day:
                self.draw_date(now)
                previous_day = now.day

            # display image on the panel
            self.papirus.display(self.image)
            if now.minute < previous_minute:
                self.papirus.update()  # full update every hour
            else:
                self.papirus.partial_update()

            previous_minute = now.minute




    def get_temp(self):
        return '{c:.0f}'.format(c=self.sensor.getTempCFloat()) + u"\u00b0" + 'C'


    def clear_display_buffer(self):
        self.draw.rectangle((0, 0, self.width, self.height), fill=self.WHITE, outline=self.WHITE)
        self.draw.rectangle((1, 1, self.width - 2, self.height - 2), fill=self.WHITE, outline=self.BLACK)


    def draw_clock(self, time):
        self.draw.rectangle((2, 3, 48, 15), fill=self.WHITE, outline=self.WHITE)
        self.draw.text((3, 3), '{h:02d}{sep}{m:02d}'.format(h=time.hour, m=time.minute, sep=':' if time.second & 1 else ' '),
                  fill=self.BLACK, font=self.clock_font)

    def draw_date(self, time):
        self.draw.rectangle((59, 3, 150, 15), fill=self.WHITE, outline=self.WHITE)
        self.draw.text((60, 3),
                       '{y:04d}-{m:02d}-{d:02d}'.format(y=time.year, m=time.month, d=time.day), fill=self.BLACK, font=self.date_font)

    def draw_temp(self, tempC):
        self.draw.rectangle((159, 3, 197, 15), fill=self.WHITE, outline=self.WHITE)
        self.draw.text((160, 3), tempC, fill=self.BLACK, font=self.temp_font)



def main(argv):
    """main program - draw and display time and date"""
    display = Display(int(argv[0]) if len(sys.argv) > 1 else 0)
    display.run()


# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
