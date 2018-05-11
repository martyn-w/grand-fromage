# Tracker

FROM resin/raspberry-pi2-alpine:3.7

RUN apk add --no-cache --update tzdata python py-pip \
    && cp /usr/share/zoneinfo/Europe/London /etc/localtime \
    && echo "Europe/London" > /etc/timezone \
    && apk del tzdata \
    && pip install --upgrade pip \
    && pip install paho-mqtt gps3 geopy


COPY ./bin/docker-entrypoint.sh /bin/
COPY ./grandfromage/ /grandfromage/


CMD ["bash", "/bin/docker-entrypoint.sh"]





# FROM resin/raspberrypi3-alpine-python

#FROM resin/rpi-raspbian:jessie

## Install needed packages
#RUN apt-get -q update \
#    && apt-get -qy install \
#    git bc i2c-tools \
#    pkg-config make gcc \
#    python-smbus python-dateutil python-pip vim \
#    # Remove package lists to free up space
#    && rm -rf /var/lib/apt/lists/*


# install mqtt and gps python libraries
#RUN

