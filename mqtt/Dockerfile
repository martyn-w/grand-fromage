# Based on https://github.com/pascaldevink/rpi-mosquitto

FROM resin/rpi-raspbian:jessie

RUN apt-get -q update \
    && apt-get install -qy wget \
    && wget -q -O - http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add - \
    && wget -q -O /etc/apt/sources.list.d/mosquitto-jessie.list http://repo.mosquitto.org/debian/mosquitto-jessie.list \
    && apt-get -q update \
    && apt-get install -qy mosquitto \
    # Remove package lists to free up space
    && rm -rf /var/lib/apt/lists/*

RUN adduser --system --disabled-password --disabled-login mosquitto

COPY ./config /mqtt/config

CMD /usr/sbin/mosquitto -c /mqtt/config/mosquitto.conf
