import os
import librosa
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime


class RaspberryPi:
    def __init__(self, microphone=True, speakers=True):
        self.microphone = microphone
        self.speakers = speakers

    def play_sound(self, wav_file, save_png=False):
        print("Playing audio...")
        audio = AudioSegment.from_wav(wav_file)
        play(audio)
        if save_png:
            wav_samples = np.array(audio.get_array_of_samples())
            plt.plot(wav_samples)

            # save png with timestamp
            os.makedirs("output", exist_ok=True)
            date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            out_path = "output/fig_%s.png" % date_time
            plt.savefig(out_path)
            plt.clf()

    def record_sound(self, duration, fs=16000):
        # record voice for specified duration
        print("Recording sound...")
        myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype="float32")
        sd.wait()

        # save file with timestamp
        os.makedirs("output", exist_ok=True)
        date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        rec_path = "output/recording_%s.wav" % date_time
        print("Saving recording %s..." % rec_path)
        librosa.output.write_wav(rec_path, myrecording, fs)

        return myrecording, rec_path
