import sounddevice as sd
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.io.wavfile import write
from raspberry.util import gaussian_smooth


class Microphone:
    def __init__(
        self,
        lcd,
        sampling_rate=16000,
        volume_threshold=0.4,
        save_location="/home/pi/mnt/gdrive/recordings",
    ):
        self.lcd = lcd
        self.save_location = save_location
        self.sampling_rate = sampling_rate
        self.volume_threshold = volume_threshold

    def button_held_to_record(self, duration):
        self.lcd.display("About to\nrecord")
        time.sleep(2)
        self.lcd.display("Recording\nsound...")
        myrecording = self.record_sound(duration)
        self.lcd.display("Playing\nrecording...")
        self.play_recording(myrecording)
        self.save_recording(myrecording)
        self.lcd.display(self.lcd.waiting_message)

    def background_volume(self, duration):
        myrecording = self.record_sound(duration)
        volume = self.get_volume(myrecording)

        if volume.max() > self.volume_threshold:
            self.lcd.display(f"NOISE DETECTED\nLEVEL: {volume.max()*100:.1f}")
            self.save_recording(myrecording)
            self.play_recording(myrecording)
            self.lcd.display(self.lcd.waiting_message)

    def record_sound(self, duration):
        samples = self.sampling_rate * duration
        myrecording = sd.rec(
            samples, samplerate=self.sampling_rate, channels=1, dtype="float32"
        )
        sd.wait()
        return myrecording

    def play_recording(self, myrecording):
        sd.play(myrecording, self.sampling_rate)
        sd.wait()

    def save_recording(self, recording):
        recording = np.squeeze(recording)
        date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

        out_wav = f"{self.save_location}/{date_time}.wav"
        write(out_wav, self.sampling_rate, recording)

        out_fig = f"{self.save_location}/{date_time}.png"
        plt.plot(recording)
        plt.savefig(out_fig)
        plt.clf()

    def get_volume(self, x):
        return gaussian_smooth(np.abs(np.squeeze(x)))
