#!/bin/bash

# Prepares a Raspberry Pi to run GrandFromage: Monitor

# 1. General setup
echo "127.0.0.1       GrandFromageMonitor" | sudo tee -a /etc/hosts
echo "GrandFromageMonitor" | sudo tee /etc/hostname

# Reduce GPU memory as we are running headless
sudo sed -i 's/gpu_mem\=128/gpu_mem=16/' /boot/config.txt


# 2. Download and install docker
curl -sSL get.docker.com | sh
sudo systemctl enable docker
sudo reboot now

