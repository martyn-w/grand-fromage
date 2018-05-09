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

    CLOCK_FONT_FILE = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
    DATE_FONT_FILE  = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'


    def __init__(self, rotation):
        self.papirus = Papirus(rotation=rotation)

        print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=self.papirus.panel, w=self.papirus.width,
                                                                                       h=self.papirus.height,
                                                                                       v=self.papirus.version, g=self.papirus.cog,
                                                                                       f=self.papirus.film))
        self.papirus.clear()
        #self.demo()


    def demo(self):
        """simple partial update demo - draw a clock"""

        # initially set all white background
        self.image = Image.new('1', self.papirus.size, self.WHITE)

        # prepare for drawing
        self.draw = ImageDraw.Draw(self.image)
        self.width, self.height = self.image.size

        clock_font_size = int(((self.width * 0.25) - 4) / (5 * 0.65))  # 5 chars HH:MM
        clock_font = ImageFont.truetype(self.CLOCK_FONT_FILE, clock_font_size)

        date_font_size = int((self.width - 10) / (10 * 0.65))  # 10 chars YYYY-MM-DD
        date_font = ImageFont.truetype(self.DATE_FONT_FILE, date_font_size)

        temp_font_size = int(((self.width * 0.5) - 4) / (5 * 0.65))  # 5 chars 29 ^C
        temp_font = ImageFont.truetype(self.DATE_FONT_FILE, temp_font_size)

        # clear the display buffer
        self.draw_border()
        self.draw.rectangle((0, 0, self.width, self.height), fill=self.WHITE, outline=self.WHITE)
        previous_minute = 0
        previous_day = 0
        sensor = LM75B()
        previous_temp = ''

        while True:
            while True:
                now = datetime.today()
                tempC = '{c:.0f}'.format(c=sensor.getTempCFloat()) + u"\u00b0" + 'C'

                if now.minute != previous_minute or tempC != previous_temp:
                    break

                time.sleep(0.5)

            if now.day != previous_day:
                self.draw.rectangle((2, 2, self.width - 2, self.height - 2), fill=self.WHITE, outline=self.BLACK)
                self.draw.text((10, clock_font_size + 10), '{y:04d}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=now.day),
                          fill=self.BLACK, font=date_font)
                previous_day = now.day
            else:
                self.draw.rectangle((5, 10, self.width - 5, 10 + clock_font_size), fill=self.WHITE, outline=self.WHITE)

            # draw.text((5, 10), '{h:02d}:{m:02d}'.format(h=now.hour, m=now.minute), fill=BLACK, font=clock_font)
            self.draw_clock(now, clock_font)

            self.draw.text((104, 10), tempC, fill=self.BLACK, font=temp_font)

            # display image on the panel
            self.papirus.display(self.image)
            if now.minute < previous_minute:
                self.papirus.update()  # full update every hour
            else:
                self.papirus.partial_update()
            previous_minute = now.minute
            previous_temp = tempC


    def clear_display(self):
        print("clear display")


    def draw_border(self):
        print("draw border")


    def draw_clock(self, time, font):
        self.draw.text((5, 10), '{h:02d}{sep}{m:02d}'.format(h=time.hour, m=time.minute, sep=':' if time.second & 1 else ' '),
                  fill=self.BLACK, font=font)



def main(argv):
    """main program - draw and display time and date"""
    display = Display(int(argv[0]) if len(sys.argv) > 1 else 0)
    display.demo()


    # papirus = Papirus(rotation = )
    # print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=papirus.panel, w=papirus.width, h=papirus.height, v=papirus.version, g=papirus.cog, f=papirus.film))
    # papirus.clear()
    # demo(papirus)



# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
