FROM resin/raspberry-pi2-alpine:3.7

RUN apk update \
    && apk add gpsd tzdata \
    && cp /usr/share/zoneinfo/Europe/London /etc/localtime \
    && echo "Europe/London" > /etc/timezone \
    && apk del tzdata


COPY ./bin/docker-entrypoint.sh /bin/

CMD ["bash", "/bin/docker-entrypoint.sh"]
