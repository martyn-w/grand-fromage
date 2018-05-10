#!/bin/bash

# Set timezone
echo "${TIMEZONE=UTC}" > /etc/timezone
dpkg-reconfigure tzdata

# set USB serial port speed
stty -F /dev/ttyUSB0 ispeed 9600

# run GPSD in foreground
gpsd -D 0 -N -n -G /dev/ttyUSB0
