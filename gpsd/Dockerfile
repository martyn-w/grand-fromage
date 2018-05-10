FROM resin/rpi-raspbian:jessie

# Install needed packages
RUN apt-get -q update \
    && apt-get -qy install gpsd \
    # Remove package lists to free up space
    && rm -rf /var/lib/apt/lists/*

COPY ./bin/docker-entrypoint.sh /bin/

CMD ["bash", "/bin/docker-entrypoint.sh"]
