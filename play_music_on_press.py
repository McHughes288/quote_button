from raspberry.pi import RaspberryPi
import numpy as np
import random
import time

pi = RaspberryPi()
GPIO = pi.setup_gpio()
pi.update_available_sounds()

while True:
    for button_name, button_pin in pi.button_name_to_pin.items():
        # Detect button press
        if GPIO.input(button_pin) == GPIO.LOW:
            print(f"Button {button_name} (pin {button_pin}) was pushed!")
            
            # update sounds available in gdrive and get the relevant ones
            pi.update_available_sounds()
            available_files = pi.button_name_to_files[button_name]
            
            # play a random sound bite
            if available_files:
                sound_file_path = random.choice(available_files)
                print(sound_file_path)
                pi.play_sound(sound_file_path)
            else:
                pi.play_sound("/home/pi/mnt/gdrive/Brian/17.wav")

            while GPIO.input(button_pin) == GPIO.LOW:
                time.sleep(0.1)
