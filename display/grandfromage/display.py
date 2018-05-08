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

WHITE = 1
BLACK = 0

CLOCK_FONT_FILE = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
DATE_FONT_FILE  = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'



def main(argv):

    """main program - draw and display time and date"""

    papirus = Papirus(rotation = int(argv[0]) if len(sys.argv) > 1 else 0)
    print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=papirus.panel, w=papirus.width, h=papirus.height, v=papirus.version, g=papirus.cog, f=papirus.film))
    papirus.clear()
    demo(papirus)


def demo(papirus):
    """simple partial update demo - draw a clock"""

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    clock_font_size = int(((width*0.25) - 4)/(5*0.65))      # 5 chars HH:MM
    clock_font = ImageFont.truetype(CLOCK_FONT_FILE, clock_font_size)

    date_font_size = int((width - 10)/(10*0.65))     # 10 chars YYYY-MM-DD
    date_font = ImageFont.truetype(DATE_FONT_FILE, date_font_size)

    temp_font_size = int(((width*0.5) - 4)/(5*0.65))      # 5 chars 29 ^C
    temp_font = ImageFont.truetype(DATE_FONT_FILE, temp_font_size)

    # clear the display buffer
    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
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
            draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
            draw.text((10, clock_font_size + 10), '{y:04d}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=now.day), fill=BLACK, font=date_font)
            previous_day = now.day
        else:
            draw.rectangle((5, 10, width - 5, 10 + clock_font_size), fill=WHITE, outline=WHITE)

        #draw.text((5, 10), '{h:02d}:{m:02d}'.format(h=now.hour, m=now.minute), fill=BLACK, font=clock_font)
        draw_clock(draw, now, clock_font)

        draw.text((104, 10), tempC, fill=BLACK, font=temp_font)

        # display image on the panel
        papirus.display(image)
        if now.minute < previous_minute:
            papirus.update()    # full update every hour
        else:
            papirus.partial_update()
        previous_minute = now.minute
        previous_temp = tempC


def draw_clock(draw, time, font):
    draw.text((5, 10), '{h:02d}{sep}{m:02d}'.format(h=time.hour, m=time.minute, sep=':' if time.second & 1 else ' '), fill=BLACK, font=font)
    


# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass

