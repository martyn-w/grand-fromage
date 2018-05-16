# Tracker

#FROM resin/raspberry-pi2-alpine:3.7
FROM resin/rpi-raspbian:jessie
#
#RUN apk add --no-cache --update tzdata python py-pip \
#    && cp /usr/share/zoneinfo/Europe/London /etc/localtime \
#    && echo "Europe/London" > /etc/timezone \
#    && apk del tzdata \
#    && pip install --upgrade pip \
#    && pip install paho-mqtt


COPY ./bin/docker-entrypoint.sh /bin/
COPY ./grandfromage/ /grandfromage/


CMD ["bash", "/bin/docker-entrypoint.sh"]

