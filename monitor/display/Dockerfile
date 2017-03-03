FROM resin/rpi-raspbian:latest

# Install libraries
RUN apt-get -q update && \
    apt-get -qy install \
    git build-essential pkg-config curl \
    python python-imaging \
    libfuse-dev

RUN cd / && \
    git clone https://github.com/repaper/gratis.git repaper-gratis && \
    cd /repaper-gratis/ && \
    make rpi PANEL_VERSION=V231_G2 && \
    make rpi-install PANEL_VERSION=V231_G2






# RUN cd / && git clone https://github.com/PiSupply/PaPiRus.git

# RUN cd /PaPiRus/ && python setup.py install

# RUN mkdir -p /tmp/papirus && cd /tmp/papirus && git clone https://github.com/repaper/gratis.git

#RUN cd /tmp/papirus/gratis/PlatformWithOS && make rpi-epd_fuse && make rpi-install PANEL_VERSION=V231_G2

#CMD service epd-fuse start && papirus-clock

# sudo apt-get install fonts-freefont-ttf -y

# make rpi-epd_fuse PANEL_VERSION=V231_G2
# make CFLAGS="-D_FILE_OFFSET_BITS=64 -I/usr/include/fuse"  rpi-epd_fuse PANEL_VERSION=V231_G2