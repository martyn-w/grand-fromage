#!/bin/bash

# Set timezone
echo "${TIMEZONE=UTC}" > /etc/timezone
dpkg-reconfigure tzdata

# Ensure correct permissions on mosquitto folders
mkdir -p /mosquitto/log /mosquitto/data
chown -Rf mosquitto:mosquitto /mosquitto/log /mosquitto/data


# Start mosquitto
/usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf
