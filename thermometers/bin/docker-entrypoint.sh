#!/bin/bash

modprobe i2c-bcm2708
modprobe i2c-dev


while :
do
  echo "sleeping"
  sleep 60
done