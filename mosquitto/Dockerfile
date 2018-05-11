# Mosquitto

FROM resin/raspberry-pi2-alpine:3.7

RUN apk add --no-cache --update tzdata mosquitto \
    && cp /usr/share/zoneinfo/Europe/London /etc/localtime \
    && echo "Europe/London" > /etc/timezone \
    && apk del tzdata 
    #&& adduser -S -D mosquitto

COPY ./config /mosquitto/config
COPY ./bin/docker-entrypoint.sh /bin/

CMD ["bash", "/bin/docker-entrypoint.sh"]





## Based on https://github.com/pascaldevink/rpi-mosquitto
#
#FROM resin/rpi-raspbian:jessie
#
#RUN apt-get -q update \
#    && apt-get -qy install wget \
#    && wget -q -O - http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add - \
#    && wget -q -O /etc/apt/sources.list.d/mosquitto-jessie.list http://repo.mosquitto.org/debian/mosquitto-jessie.list \
#    && apt-get -q update \
#    && apt-get -qy install mosquitto \
#    # Remove package lists to free up space
#    && rm -rf /var/lib/apt/lists/*
#
#RUN adduser --system --disabled-password --disabled-login mosquitto
#
#COPY ./config /mosquitto/config
#COPY ./bin/docker-entrypoint.sh /bin/docker-entrypoint.sh
#
#CMD ["bash", "/bin/docker-entrypoint.sh"]