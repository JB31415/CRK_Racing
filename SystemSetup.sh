#!/usr/bin/bash

# Run this script as root only
if [ $UID -gt 0 ]
then
  echo "Run me as root! Exiting..."
  exit 2
fi

# Install required system packages

apt update
apt install -y tmux python3 python3-pip python3-venv python3-smbus libzbar0 i2c-tools python3-dev python3-pyqt5 python3-opencv libopencv-dev python3-pil python3-tk