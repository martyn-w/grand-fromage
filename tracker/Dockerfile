# Tracker

FROM resin/raspberry-pi2-alpine:3.7

RUN apk add --no-cache --update tzdata python py-pip gcc python-dev linux-headers musl-dev \
    && cp /usr/share/zoneinfo/Europe/London /etc/localtime \
    && echo "Europe/London" > /etc/timezone \
    && apk del tzdata \
    && apk add --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ py-smbus \
    && pip install --upgrade pip \
    && pip install paho-mqtt gps3 geopy pyownet apscheduler Adafruit_BMP


COPY ./bin/docker-entrypoint.sh /bin/
COPY ./grandfromage/ /grandfromage/


CMD ["bash", "/bin/docker-entrypoint.sh"]
