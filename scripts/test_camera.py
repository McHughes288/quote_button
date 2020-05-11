from picamera import PiCamera
from time import sleep
import os

camera = PiCamera()

camera.start_preview()
for i in range(5):
    sleep(5)
    camera.capture("/home/pi/mnt/gdrive/images/image%s.jpg" % i)
camera.stop_preview()

os.popen("/home/pi/git/quote_button/scripts/gdrive_sync.sh")
