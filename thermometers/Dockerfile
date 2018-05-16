# Thermometers

FROM resin/rpi-raspbian:stretch

# Install needed packages
RUN apt-get -q update \
    && apt-get -qy install \
    i2c-tools owfs \
    # Remove package lists to free up space
    && rm -rf /var/lib/apt/lists/*


#
#RUN apk add --no-cache --update tzdata python py-pip \
#    && cp /usr/share/zoneinfo/Europe/London /etc/localtime \
#    && echo "Europe/London" > /etc/timezone \
#    && apk del tzdata \
#    && pip install --upgrade pip \
#    && pip install paho-mqtt
#
#RUN apt-get update \
#    && apt-get install i2c-tools owfs ow-shell



COPY ./bin/docker-entrypoint.sh /bin/
COPY ./grandfromage/ /grandfromage/
COPY ./conf/owfs.conf /etc/owfs.conf


CMD ["bash", "/bin/docker-entrypoint.sh"]
