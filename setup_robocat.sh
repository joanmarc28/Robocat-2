#!/bin/bash

set -e 

echo "Actualitzant llistes de paquets..."
sudo apt update

echo "Instal·lant dependències del sistema..."
sudo apt install -y \
build-essential cmake pkg-config \
libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev \
libv4l-dev v4l-utils \
libxvidcore-dev libx264-dev \
libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev \
libgtk-3-dev libcanberra-gtk3-dev \
libatlas-base-dev gfortran \
libhdf5-dev libhdf5-serial-dev libqt5gui5 libopenjp2-7-dev libopenexr-dev \
libgstreamer1.0-dev libimath-dev libreadline-dev libncurses-dev \
libudev-dev libfreetype6-dev libharfbuzz-dev libxcb1-dev libffi-dev

echo "Eliminant entorn antic si existeix..."
rm -rf robocat_env

echo "Creant nou entorn virtual..."
python3 -m venv robocat_env
source robocat_env/bin/activate

echo "⬆Actualitzant pip..."
pip install --upgrade pip

echo "Instal·lant llibreries de Python (pot trigar uns minuts)..."
pip install numpy==1.23.5 tensorflow==2.13.0 opencv-python-headless

echo "Instal·lant la resta del requirements..."
cat > requirements_robocat.txt <<EOF
adafruit-blinka
adafruit-circuitpython-busdevice
adafruit-circuitpython-connectionmanager
adafruit-circuitpython-framebuf
adafruit-circuitpython-motor
adafruit-circuitpython-pca9685
adafruit-circuitpython-register
adafruit-circuitpython-requests
adafruit-circuitpython-ssd1306
adafruit-circuitpython-typing
adafruit-platformdetect
adafruit-pureio
aiohttp
aioice
aiortc
aiosignal
async-timeout
attrs
av
binho-host-adapter
cbor2
certifi
cffi
charset-normalizer
click
cryptography
dnspython
docker
frozenlist
google-crc32c
idna
ifaddr
jsonschema
jsonschema-specifications
keyboard
libarchive-c
luma
luma-core
luma-oled
mpu6050
picamera
picamera2
pidng
piexif
pillow
propcache
pycparser
pyee
pyftdi
pygame
pylibsrtp
pyopenssl
pyparsing
pyserial
python-dateutil
python-prctl
pyusb
quat
referencing
requests
rpds-py
rpi-gpio
setuptools
simplejpeg
six
smbus2
spidev
sysv-ipc
tk
toml
tqdm
typing-extensions
tzdata
urllib3
v4l2-python3
websockets
yarl
ultralytics
scikit-learn
Pillow
luma.core
luma.oled
EOF

pip install -r requirements_robocat.txt

pip install --index-url https://pypi.org/simple speechrecognition

echo "Verificant numpy..."
python3 -c "import numpy; print('numpy version:', numpy.__version__, '| path:', numpy.__file__)"

echo "Instal·lació finalitzada correctament!"
