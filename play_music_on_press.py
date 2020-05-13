from raspberry.pi import RaspberryPi
from raspberry.camera import Camera
import numpy as np
import random
import time
from multiprocessing import Process

pi = RaspberryPi()
pi.setup_gpio()
pi.update_available_sounds()

camera = Camera(pi, greeting_sound="/home/pi/mnt/gdrive/Brian/17.wav")

flash_process = None
wait_process = None
# camera.detect_motion()
# camera.camera.close()

try:
    while True:
        # LED turn on in waves for "waiting" state
        if wait_process is None or not wait_process.is_alive():
            if flash_process is None or not flash_process.is_alive():
                wait_process = Process(target=pi.wave_leds, args=(0.1,))
                wait_process.start()

        for button_name in pi.button_names:
            # Detect button press
            if pi.button_pressed(button_name):
                print(f"Button {button_name} was pushed!")
                wait_process.terminate()

                # Terminate flashing led process if running
                if flash_process is not None and flash_process.is_alive():
                    print("Terminating flash led process...")
                    flash_process.terminate()
                    pi.turn_leds_off()

                # update sounds available in gdrive and get the relevant ones
                pi.update_available_sounds()
                available_files = pi.button_name_to_files[button_name]
                
                # pick a random sound bite
                if available_files:
                    sound_file_path = random.choice(available_files)  
                else:
                    sound_file_path = "/home/pi/mnt/gdrive/Brian/17.wav"
                print(sound_file_path)
                
                # Flash LEDs as background process and play sound
                flash_process = Process(target=pi.flash_to_sound, args=(sound_file_path,))
                flash_process.start()
                pi.play_sound(sound_file_path)

                # if button still held, just wait
                while pi.button_pressed(button_name):
                    time.sleep(0.05)
except KeyboardInterrupt:
    pass
pi.GPIO.cleanup()
camera.camera.close()