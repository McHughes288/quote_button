import sounddevice as sd
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.io.wavfile import write
from raspberry.util import gaussian_smooth


class Microphone:
    def __init__(
        self, lcd, sampling_rate=16000, save_location="/home/pi/mnt/gdrive/recordings"
    ):
        self.lcd = lcd
        self.save_location = save_location
        self.sampling_rate = sampling_rate

    def record_sound(self, duration, playback=True, save_wav=True):
        self.lcd.display("About to\nrecord...")
        time.sleep(2)

        # record voice for specified duration
        self.lcd.display("Recording\nsound...")
        samples = self.sampling_rate * duration
        myrecording = sd.rec(
            samples, samplerate=self.sampling_rate, channels=1, dtype="float32"
        )
        sd.wait()

        if save_wav:
            self.save_recording(myrecording)

        if playback:
            self.lcd.display("Playing\nrecording...")
            sd.play(myrecording, self.sampling_rate)
            sd.wait()

        self.lcd.display(self.lcd.waiting_message)

    def save_recording(self, recording):
        recording = np.squeeze(recording)
        date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

        out_wav = f"{self.save_location}/{date_time}.wav"
        write(out_wav, self.sampling_rate, recording)

        out_fig = f"{self.save_location}/{date_time}.png"
        plt.plot(recording)
        plt.savefig(out_fig)
        plt.clf()

    def rage_present(x):
        x = np.squeeze(x).abs()
        x = gaussian_smooth(x)
        if x.max() > 0.4:
            return True
