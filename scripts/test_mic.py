import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

def wav_to_float(x):
    """
    Input in range -2**15, 2**15 (or what is determined from dtype)
    Output in range -1, 1
    """
    min_value = np.iinfo(x.dtype).min
    max_value = np.iinfo(x.dtype).max

    x = x.astype(np.float32)

    x = x - min_value
    x = x / ((max_value - min_value) / 2.0)
    x = x - 1.0
    return x

fs = 16000
duration = 4  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype="int16")
print("Recording Audio 1")
sd.wait()

myrecording = np.squeeze(myrecording)
print(myrecording.shape, myrecording.max())
print(type(myrecording[0]))


print("Play Audio")
sd.play(myrecording, fs)
sd.wait()

write("/home/pi/test.wav", fs, myrecording)

myrecording = wav_to_float(myrecording)

print(myrecording.shape, myrecording.max())
print(type(myrecording[0]))
