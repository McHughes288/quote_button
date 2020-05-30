from raspberry.microphone import Microphone
from raspberry.lcd import LCDScreen

lcd = LCDScreen(waiting_message="Waiting...")
mic = Microphone(lcd)

while True:
    mic.record_sound(10, playback=False, save_wav=True)
