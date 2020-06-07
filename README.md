# Quote Button
Raspberry pi powered quote button that responds to visual and audio inputs and plays sound bites.

## Setup

* Run setup to install requirements `cd /home/pi/git/quote_button && ./scripts/setup.sh`
* Connect LEDs and buttons as done here: https://www.makeuseof.com/tag/add-button-raspberry-pi-project/ (change pin numbers and folder names in class raspberry/pi.py)
* Connect LCD as done here: https://learn.adafruit.com/character-lcds/python-circuitpython (Section "Raspberry Pi wired to a single color backlight character LCD")
* Setup night vision camera as done here: https://thepihut.com/blogs/raspberry-pi-tutorials/installing-the-raspberry-pi-camera-board
* Google Drive setup: https://medium.com/@artur.klauser/mounting-google-drive-on-raspberry-pi-f5002c7095c2 (add `*/2 * * * * $ROOT_CLONE/scripts/gdrive_sync.sh` to crontab)
* Start on boot by adding this to the crontab: `@reboot /home/pi/git/quote_button/run.sh`