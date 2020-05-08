
import sounddevice as sd
import numpy as np

fs=16000
duration = 8  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float32')
print("Recording Audio")
sd.wait()

print("Play Audio")
sd.play(myrecording, fs)
sd.wait()

myrecording = np.squeeze(myrecording)
print(myrecording.shape)
print(type(myrecording[0]))