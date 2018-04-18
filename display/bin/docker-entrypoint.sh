#!/bin/bash

# Set timezone
echo "${TIMEZONE=UTC}" > /etc/timezone
dpkg-reconfigure tzdata

# Make sure i2c is loaded
modprobe i2c-dev

# Start the fuse driver
systemctl start epd-fuse.service

python /bin/display.py
