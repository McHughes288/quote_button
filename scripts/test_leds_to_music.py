from scipy.io.wavfile import read
import numpy as np
from raspberry.pi import RaspberryPi
from raspberry.util import start_pwm, dim_leds, stop_pwm, get_sample_rate
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--soundfile",
    "-s",
    action="store",
    default="/home/pi/mnt/gdrive/Brian/the_bart_of_technology.wav",
    dest="soundfile",
)
args = parser.parse_args()

sound = read(args.soundfile)
sampling_rate = get_sample_rate(args.soundfile)

sound = np.array(sound[1], dtype=float)
mono = sound[:,0] + sound[:,1] / 2.0
print(mono.shape)
print(mono.shape[0]/sampling_rate)
print(mono.max(), mono.min())

rescale = abs(mono) / abs(mono).max()
print(rescale.max(), rescale.min())

remainder = int(rescale.shape[0] % (sampling_rate * 0.01))
rescale_subsample = rescale[0:-remainder]
print(remainder, rescale.shape, rescale_subsample.shape)
rescale_subsample = rescale_subsample.reshape(-1, int(sampling_rate * 0.01))
print(rescale_subsample.shape)
rescale_subsample = np.max(rescale_subsample, 1)
print(rescale_subsample.shape)


pi = RaspberryPi()
GPIO = pi.setup_gpio()
pwm_pins = start_pwm(pi.led_pins, GPIO)

pi.play_sound(args.soundfile)

for sample in rescale_subsample:
    if sample > 0.8:
        dim_leds(pwm_pins, 1, wait=0.01)
    else:
        dim_leds(pwm_pins, 0, wait=0.01)

stop_pwm(pwm_pins, GPIO)


