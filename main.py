from raspberry.pi import RaspberryPi
from raspberry.camera import Camera
from raspberry.lcd import LCDScreen
from raspberry.microphone import Microphone
from raspberry.util import get_available_sounds, play_sound
import numpy as np
import random
import time
from multiprocessing import Process

pi = RaspberryPi()
pi.setup_gpio()

camera = Camera(greeting_sound="/home/pi/mnt/gdrive/Brian/17.wav")
lcd = LCDScreen(waiting_message="BRESS ME\nPLEASE SIR")
mic = Microphone(lcd)

flash_process = None
wait_process = None
lcd_process = None

loop_count = 0
loop_times = []
fps_times = []
t_cam = time.time()

try:
    while 1:
        t = time.time()

        # If an audio clip isn't being played (hence the flash process)
        if flash_process is None or not flash_process.is_alive():

            # LED turn on in waves for "waiting" state
            if wait_process is None or not wait_process.is_alive():
                wait_process = Process(target=pi.leds.wave, args=(0.1,))
                wait_process.start()

            # Take picture every 15 loops
            if loop_count % 10 == 0:
                fps_times.append(time.time() - t_cam)
                t_cam = time.time()
                camera.camera.capture(
                    camera.rawCapture, format="bgr", use_video_port=True
                )
                camera.rawCapture.truncate(0)
                motion = camera.detect_motion(camera.rawCapture)
                if motion:
                    # Flash LEDs as background process and play greeting
                    wait_process.terminate()
                    if lcd_process is not None and lcd_process.is_alive():
                        lcd_process.terminate()

                    flash_process = Process(
                        target=pi.leds.flash_to_sound, args=(camera.greeting_sound,)
                    )
                    flash_process.start()

                    lcd_process = Process(target=lcd.scroll, args=("BELLO THERE!",))
                    lcd_process.start()

                    play_sound(camera.greeting_sound)

        # Detect button press for each button
        for button_name in pi.buttons.names:
            if pi.buttons.pressed(button_name):

                wait_process.terminate()
                camera.reset_detection()
                pi.leds.turn_on()

                # if button still held, just wait
                # record and play if over 3 seconds
                total_time = 0
                while pi.buttons.pressed(button_name):
                    total_time += 0.05
                    time.sleep(0.05)

                    if total_time > 3:
                        mic.record_sound(5)
                        break
                if total_time > 3:
                    break

                print(f"Button {button_name} was pushed!")

                # Terminate flashing led process if running
                if flash_process is not None and flash_process.is_alive():
                    print("Terminating flash led process...")
                    flash_process.terminate()
                    pi.leds.turn_off()
                if lcd_process is not None and lcd_process.is_alive():
                    lcd_process.terminate()

                # get sounds available in gdrive for relevant button
                available_files = get_available_sounds(button_name)

                # pick a random sound bite
                if available_files:
                    sound_file_path = random.choice(available_files)
                else:
                    sound_file_path = "/home/pi/mnt/gdrive/Brian/17.wav"
                print(sound_file_path)

                # Flash LEDs in background
                flash_process = Process(
                    target=pi.leds.flash_to_sound, args=(sound_file_path,)
                )
                flash_process.start()
                # Scroll LCD in background
                lcd_process = Process(
                    target=lcd.scroll, args=(sound_file_path.split("/")[-1],)
                )
                lcd_process.start()

                play_sound(sound_file_path)

        loop_times.append(time.time() - t)
        loop_count = loop_count + 1
except KeyboardInterrupt:
    pass
finally:
    lcd.turn_off()
    camera.camera.close()
    pi.terminate()
    print(f"Average loop time: {np.array(loop_times).mean():.6f}")
    print(f"Average fps: {1/np.array(fps_times).mean():.2f}")
