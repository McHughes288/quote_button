from raspberry.pi import RaspberryPiZero
from raspberry.util import get_available_sounds, play_sound
import numpy as np
import random
import time
from multiprocessing import Process

pi = RaspberryPiZero()
pi.setup_gpio()

flash_process = None
wait_process = None

try:
    while 1:
        # If an audio clip isn't being played (hence the flash process)
        if flash_process is None or not flash_process.is_alive():
            # LED turn on in waves for "waiting" state
            if wait_process is None or not wait_process.is_alive():
                wait_process = Process(target=pi.leds.wave, args=(0.6,))
                wait_process.start()


        # Detect button press for each button
        for button_name in pi.buttons.names:
            if pi.buttons.pressed(button_name):

                wait_process.terminate()

                # if button still held, just wait
                total_time = 0
                level = 0
                pi.leds.turn_off()
                pi.leds.start_pwm()
                while pi.buttons.pressed(button_name):
                    total_time += 0.05
                    time.sleep(0.05)

                    pi.leds.set_brightness(level)
                    if total_time < 3:
                        level = level + (100 * 0.05 / 3)

                pi.leds.stop_pwm()
                pi.leds.turn_on()

                print(f"Button {button_name} was pushed!")

                # Terminate flashing led process if running
                if flash_process is not None and flash_process.is_alive():
                    print("Terminating flash led process...")
                    flash_process.terminate()
                    pi.leds.turn_off()

                # get sounds available in gdrive for relevant button
                available_files = get_available_sounds(button_name)

                # pick a random sound bite
                if available_files:
                    sound_file_path = random.choice(available_files)
                else:
                    continue
                print(sound_file_path)

                # Flash LEDs in background
                flash_process = Process(
                    target=pi.leds.flash_to_sound, args=(sound_file_path,)
                )
                flash_process.start()

                play_sound(sound_file_path)

except KeyboardInterrupt:
    pass
finally:
    pi.terminate()
