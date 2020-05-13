# import os
# import librosa
# import numpy as np
# import sounddevice as sd
# import matplotlib.pyplot as plt
# from pydub import AudioSegment
# from pydub.playback import play
# from datetime import datetime
import pygame
import RPi.GPIO as GPIO
import os
from raspberry.util import get_sample_rate
from scipy.io.wavfile import read
import numpy as np
import time

class RaspberryPi:
    def __init__(self, microphone=False, speakers=True, camera=True):
        self.microphone = microphone
        self.speakers = speakers
        self.camera = camera

        self.GPIO = GPIO

        self.button_names = ["Brian", "Mowbros", "Random", "Alert"]

        self.button_name_to_pin = {
            "Brian": 38, 
            "Mowbros": 32, 
            "Random": 40, 
            "Alert": 36
        }

        self.button_name_to_files = {
            "Brian": [], 
            "Mowbros": [], 
            "Random": [], 
            "Alert": []
        }

        self.led_pins = [7, 11, 12, 16, 29, 31]
    
    def setup_gpio(self):
        self.GPIO.setmode(self.GPIO.BOARD)
        
        # button pins
        for pin in self.button_name_to_pin.values():
            self.GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # LED pins
        for pin in self.led_pins:
            self.GPIO.setup(pin, GPIO.OUT)
        
    def update_available_sounds(self):
        for name in self.button_name_to_files.keys():
            sound_file_paths = []
            folder_path = f"/home/pi/mnt/gdrive/{name}"
            for (dirpath, dirnames, filenames) in os.walk(folder_path):
                sound_file_paths.extend([f"{dirpath}/{name}" for name in filenames])
            self.button_name_to_files[name] = sound_file_paths

    def play_sound(self, sound_file_path, wait_to_finish=False):
        sampling_rate = get_sample_rate(sound_file_path)

        pygame.mixer.init(frequency=sampling_rate)
        pygame.mixer.music.load(sound_file_path)
        pygame.mixer.music.play()

        if wait_to_finish:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
    
    def button_pressed(self, button_name):
        button_pin = self.button_name_to_pin[button_name]
        return self.GPIO.input(button_pin) == self.GPIO.LOW

    def flash_to_sound(self, sound_file_path, update_every=0.01):
        sound = read(sound_file_path)
        sampling_rate = get_sample_rate(sound_file_path)

        sound = np.array(sound[1], dtype=float)
        mono = sound[:,0] + sound[:,1] / 2.0
        loudness = abs(mono) / abs(mono).max()

        # downsample by max pooling over update_every chunks
        remainder = int(loudness.shape[0] % (sampling_rate * update_every))
        loudness = loudness[0:-remainder]
        loudness = loudness.reshape(-1, int(sampling_rate * update_every))
        loudness = np.max(loudness, 1)

        # LEDs on if over a volume threshold
        for level in loudness:
            if level > 0.6:
                self.turn_leds_on()
            else:
                self.turn_leds_off()
            time.sleep(update_every)
        
        self.turn_leds_off()

    def turn_leds_on(self):
        for pin in self.led_pins:
            self.GPIO.output(pin, self.GPIO.HIGH)

    def turn_leds_off(self):
        for pin in self.led_pins:
            self.GPIO.output(pin, self.GPIO.LOW)

    def wave_leds(self, length):
        time.sleep(1)
        while 1:
            for pin in self.led_pins:
                self.GPIO.output(pin, self.GPIO.HIGH)
                time.sleep(length)
            for pin in self.led_pins:
                self.GPIO.output(pin, self.GPIO.LOW)
                time.sleep(length)



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
