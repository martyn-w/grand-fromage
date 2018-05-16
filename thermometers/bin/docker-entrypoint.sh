#!/bin/bash

# Set timezone
echo "${TIMEZONE=UTC}" > /etc/timezone
dpkg-reconfigure tzdata

# modprobe i2c-bcm2708
# modprobe i2c-dev

echo "Starting owserver"
owserver -c /etc/owfs.conf

echo "Running owhttpd"
owhttpd --foreground -c /etc/owfs.conf


# while :
# do
#  echo "sleeping"
#  sleep 60
# done
