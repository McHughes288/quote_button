#!/bin/bash

VENV=$HOME/venv
ROOT_CLONE=$HOME/git/quote_button

echo "Installing system requirements..."
# sudo apt install libblas-dev llvm python3-pip python3-scipy
sudo apt-get install rclone # google drive
sudo apt-get install python3-opencv libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5 # open cv
sudo apt-get install python-rpi.gpio python3-rpi.gpio # gpio
sudo apt-get libatlas-base-dev # microphone

# git clone https://github.com/pimylifeup/Adafruit_Python_CharLCD.git $HOME/git
# cd $HOME/git/Adafruit_Python_CharLCD && sudo python setup.py install

if [ ! -d $VENV ]; then
echo "Creating $VENV"
    pip install virtualenv
    virtualenv --system-site-packages -p python3 $VENV
fi

echo "Starting venv..."
source $VENV/bin/activate

echo "Installing python modules..."

pip3 install -r $ROOT_CLONE/requirements.txt

echo "Syncing google drive..."
$ROOT_CLONE/scripts/gdrive_sync.sh
