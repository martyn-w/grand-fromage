# Based on https://github.com/resin-io-playground/resinio-PaPiRus

FROM resin/rpi-raspbian:jessie

# Install needed packages
RUN apt-get -q update \
    && apt-get -qy install \
    libfuse-dev fonts-freefont-ttf \
    git bc i2c-tools \
    pkg-config make gcc \
    python-imaging python-smbus python-dateutil python-pip vim \
    # Remove package lists to free up space
    && rm -rf /var/lib/apt/lists/*


# Install the EPD driver
# Known to work with git commit 27f245ed4a4ff391b721a0a30c7f952b2266a690   (19-Dec-2017)
RUN mkdir -p /tmp/gratis \
    && git clone https://github.com/repaper/gratis.git /tmp/gratis \
    && cd /tmp/gratis/ \
    && git checkout 27f245ed4a4ff391b721a0a30c7f952b2266a690 \
    && make rpi EPD_IO=epd_io.h PANEL_VERSION='V231_G2' \
    && make rpi-install EPD_IO=epd_io.h PANEL_VERSION='V231_G2' \
    && cd / \
    && rm -rf /tmp/gratis

# Install PaPiRus
# Known to work with git commit dc942764e4694b8f91b65f74d81f9a2fe85a7521  (20-Jan-2018)
RUN mkdir -p /tmp/papirus \
    && git clone https://github.com/PiSupply/PaPiRus.git /tmp/papirus \
    && cd /tmp/papirus \
    && git checkout dc942764e4694b8f91b65f74d81f9a2fe85a7521 \
    && python setup.py install \
    && cd / \
    && rm -rf /tmp/papirus

# install mqtt python libraries
RUN pip install paho-mqtt

COPY ./epd-fuse/epd-fuse.configuration /etc/default/epd-fuse
COPY ./bin/docker-entrypoint.sh /bin/
COPY ./grandfromage/ /grandfromage/

# Systemd please
ENV INITSYSTEM on

CMD ["bash", "/bin/docker-entrypoint.sh"]
