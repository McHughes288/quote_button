#!/bin/bash

VENV=$HOME/venv
ROOT_CLONE=$HOME/git/quote_button

echo "Installing system requirements..."
sudo apt-get -y install python3-pip # python packages
sudo apt-get -y install rclone # google drive
sudo apt-get -y install python3-opencv libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5 # open cv
sudo apt-get -y install python-rpi.gpio python3-rpi.gpio # gpio
sudo apt-get -y install libatlas-base-dev # microphone
sudo apt-get -y install mplayer libsdl-mixer1.2 # speakers

if [ ! -d $VENV ]; then
echo "Creating $VENV"
    pip3 install virtualenv
    virtualenv --system-site-packages -p python3 $VENV
fi

echo "Starting venv..."
source $VENV/bin/activate

echo "Installing python modules..."
pip3 install -r $ROOT_CLONE/requirements.txt
