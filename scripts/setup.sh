#!/bin/bash

VENV=$HOME/venv
ROOT_CLONE=$HOME/git/quote_button

if [ ! -d $VENV ]; then
echo "Creating $VENV"
    pip install virtualenv
    virtualenv -p python3 $VENV
fi

echo "Starting venv..."
source $VENV/bin/activate

echo "Installing requirements..."
# sudo apt install libblas-dev llvm python3-pip python3-scipy
sudo apt-get install rclone libportaudio2 libatlas-base-dev
pip3 install -r $ROOT_CLONE/requirements.txt

$ROOT_CLONE/scripts/gdrive_sync.sh
