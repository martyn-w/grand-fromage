# Based on https://github.com/resin-io-playground/resinio-PaPiRus

FROM resin/rpi-raspbian:latest

# Install needed packages
RUN apt-get -q update \
    && apt-get -qy install \
    git pkg-config python-imaging libfuse-dev \
    fonts-freefont-ttf bc i2c-tools make  gcc \
    python python-smbus \
    # Remove package lists to free up space
    && rm -rf /var/lib/apt/lists/*


# Install the EPD driver
# Known to work with git commit 81e45907b052fbc52412ccb7bc51404c42df0764   (30-Mar-2017)
RUN mkdir -p /tmp/gratis \
    && git clone https://github.com/repaper/gratis.git /tmp/gratis \
    && cd /tmp/gratis/ \
    && make rpi PANEL_VERSION=V231_G2 \
    && make rpi-install PANEL_VERSION=V231_G2 \
    && cd / \
    && rm -rf /tmp/gratis \


# Install PaPiRus
# Known to work with git commit 7a690722d5f9f73705ea5d8ac2f4e034f31db271  (11-Apr-2017)
RUN mkdir /tmp/papirus \
    && git clone https://github.com/PiSupply/PaPiRus.git /tmp/papirus \
    && cd /tmp/papirus \
    && python setup.py install \
    && cd / \
    && rm -rf /tmp/papirus

COPY ./epd-fuse/epd-fuse.configuration /etc/default/epd-fuse
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh

# Systemd please
ENV INITSYSTEM on

CMD ["bash", "/app/docker-entrypoint.sh"]
