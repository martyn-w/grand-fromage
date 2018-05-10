FROM resin/rpi-raspbian:jessie

# Install needed packages
RUN apt-get -q update \
    && apt-get -qy install \
    git bc i2c-tools \
    pkg-config make gcc \
    python-smbus python-dateutil python-pip vim \
    # Remove package lists to free up space
    && rm -rf /var/lib/apt/lists/*


# install mqtt python libraries
RUN pip install paho-mqtt

COPY ./bin/docker-entrypoint.sh /bin/
COPY ./grandfromage/ /grandfromage/

# Systemd please
ENV INITSYSTEM on

CMD ["bash", "/bin/docker-entrypoint.sh"]
