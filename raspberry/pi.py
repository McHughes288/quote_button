# import librosa
# import sounddevice as sd
# import matplotlib.pyplot as plt
# from pydub import AudioSegment
# from pydub.playback import play
# from datetime import datetime

import RPi.GPIO as GPIO
import os
from raspberry.util import get_sample_rate
from raspberry.led import LEDArray
import time


class RaspberryPi:
    def __init__(self):

        self.GPIO = GPIO

        self.button_names = ["Brian", "Mowbros", "Random", "Alert"]

        self.button_name_to_pin = {
            "Brian": 20,  # 38,
            "Mowbros": 12,  # 32,
            "Random": 21,  # 40,
            "Alert": 16,  # 36,
        }

        led_pins = [4, 17, 18, 23, 5, 6]  # [7, 11, 12, 16, 29, 31]
        led_pins = led_pins[::-1]
        self.leds = LEDArray(led_pins)

    def setup_gpio(self):
        self.GPIO.setmode(self.GPIO.BCM)  # BOARD)
        self.GPIO.setwarnings(False)

        # button pins
        for pin in self.button_name_to_pin.values():
            self.GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.leds.setup()

    def button_pressed(self, button_name):
        button_pin = self.button_name_to_pin[button_name]
        return self.GPIO.input(button_pin) == self.GPIO.LOW

    def terminate(self):
        self.leds.turn_off()
        self.GPIO.cleanup()



    # def play_recording(self, wav_file, save_png=False):
    #     print("Playing audio...")
    #     audio = AudioSegment.from_wav(wav_file)
    #     play(audio)
    #     if save_png:
    #         wav_samples = np.array(audio.get_array_of_samples())
    #         plt.plot(wav_samples)

    #         # save png with timestamp
    #         os.makedirs("output", exist_ok=True)
    #         date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    #         out_path = "output/fig_%s.png" % date_time
    #         plt.savefig(out_path)
    #         plt.clf()

    # def record_sound(self, duration, fs=16000):
    #     # record voice for specified duration
    #     print("Recording sound...")
    #     myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype="float32")
    #     sd.wait()

    #     # save file with timestamp
    #     os.makedirs("output", exist_ok=True)
    #     date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    #     rec_path = "output/recording_%s.wav" % date_time
    #     print("Saving recording %s..." % rec_path)
    #     librosa.output.write_wav(rec_path, myrecording, fs)

    #     return myrecording, rec_path
