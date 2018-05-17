# OWServer

FROM resin/rpi-raspbian:stretch

# Install needed packages
RUN apt-get -q update \
    && apt-get -qy install owfs \
    # Remove package lists to free up space
    && rm -rf /var/lib/apt/lists/*

COPY ./bin/docker-entrypoint.sh /bin/
COPY ./conf/owfs.conf /etc/owfs.conf


CMD ["bash", "/bin/docker-entrypoint.sh"]
