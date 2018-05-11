#!/bin/bash

# set USB serial port speed
stty -F /dev/ttyUSB0 ispeed 9600

# run GPSD in foreground
gpsd -D 3 -N -n -G /dev/ttyUSB0
