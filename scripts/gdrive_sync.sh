#!/bin/bash

# follow rclone config instructions here:
# https://medium.com/@artur.klauser/mounting-google-drive-on-raspberry-pi-f5002c7095c2

# add to crontab by running `crontab -e` and paste:
# `*/2 * * * * $ROOT_CLONE/scripts/gdrive_sync.sh`

LOCAL_GDRIVE=$HOME/mnt/gdrive

# Create directories
if [ ! -d $LOCAL_GDRIVE ]; then
    mkdir -p $LOCAL_GDRIVE
fi
if [ ! -d $LOCAL_GDRIVE/recordings ]; then
    mkdir -p $LOCAL_GDRIVE/recordings
    touch $LOCAL_GDRIVE/recordings/init
fi
if [ ! -d $LOCAL_GDRIVE/images ]; then
    mkdir -p $LOCAL_GDRIVE/images
    touch $LOCAL_GDRIVE/images/init
fi

# First sync rpi output to remote gdrive
rclone sync $LOCAL_GDRIVE/recordings gdrive:"Badonde Button"/recordings
rclone sync $LOCAL_GDRIVE/images gdrive:"Badonde Button"/images
# Second sync all remote gdrive to rpi
rclone sync gdrive:"Badonde Button" $LOCAL_GDRIVE