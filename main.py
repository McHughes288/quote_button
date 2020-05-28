from raspberry.pi import RaspberryPi
from raspberry.camera import Camera
from raspberry.lcd import LCDScreen
from raspberry.util import get_available_sounds
import numpy as np
import random
import time
from multiprocessing import Process

pi = RaspberryPi()
pi.setup_gpio()

camera = Camera(pi, greeting_sound="/home/pi/mnt/gdrive/Brian/17.wav")
print("[CAMERA] Camera warming up...")
time.sleep(camera.camera_warmup_time)

lcd = LCDScreen(waiting_message="BRESS ME\nPLEASE SIR")

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
                wait_process = Process(target=pi.wave_leds, args=(0.1,))
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
                        target=pi.flash_to_sound, args=(camera.greeting_sound,)
                    )
                    flash_process.start()

                    lcd_process = Process(target=lcd.scroll, args=("BELLO THERE!",))
                    lcd_process.start()

                    pi.play_sound(camera.greeting_sound)

        # Detect button press for each button
        for button_name in pi.button_names:
            if pi.button_pressed(button_name):
                print(f"Button {button_name} was pushed!")
                wait_process.terminate()
                camera.reset_detection()

                # Terminate flashing led process if running
                if flash_process is not None and flash_process.is_alive():
                    print("Terminating flash led process...")
                    flash_process.terminate()
                    pi.turn_leds_off()
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
                    target=pi.flash_to_sound, args=(sound_file_path,)
                )
                flash_process.start()
                # Scroll LCD in background
                lcd_process = Process(
                    target=lcd.scroll, args=(sound_file_path.split("/")[-1],)
                )
                lcd_process.start()

                pi.play_sound(sound_file_path)

                # if button still held, just wait
                while pi.button_pressed(button_name):
                    time.sleep(0.05)

        loop_times.append(time.time() - t)
        loop_count = loop_count + 1
except KeyboardInterrupt:
    pass
finally:
    pi.turn_leds_off()
    lcd.turn_off()
    pi.GPIO.cleanup()
    camera.camera.close()
    print(f"Average loop time: {np.array(loop_times).mean():.6f}")
    print(f"Average fps: {1/np.array(fps_times).mean():.2f}")
