import sounddevice as sd
import time


class Microphone:
    def __init__(self, lcd):
        self.lcd = lcd

    def record_sound(self, duration, fs=16000):
        self.lcd.display("About to\nrecord...")
        time.sleep(2)

        # record voice for specified duration
        self.lcd.display("Recording\nsound...")
        myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype="float32")
        sd.wait()

        self.lcd.display("Playing\nrecording...")
        sd.play(myrecording, fs)
        sd.wait()

        self.lcd.display("BRESS ME\nPLEASE SIR")

    def listen_for_rage():
        pass

        # # save file with timestamp
        # os.makedirs("output", exist_ok=True)
        # date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        # rec_path = "output/recording_%s.wav" % date_time
        # print("Saving recording %s..." % rec_path)
        # librosa.output.write_wav(rec_path, myrecording, fs)

        # return myrecording, rec_path


# import librosa
# import sounddevice as sd
# import matplotlib.pyplot as plt
# from pydub import AudioSegment
# from pydub.playback import play
# from datetime import datetime
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
