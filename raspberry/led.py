import RPi.GPIO as GPIO
from scipy.io.wavfile import read
import numpy as np
import time
from raspberry.util import get_sample_rate


class LEDArray:
    def __init__(self, led_pins):
        self.led_pins = led_pins

    def setup(self):
        # LED pins
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)

        self.pwm_pins = [GPIO.PWM(pin, 100) for pin in self.led_pins]
        self.turn_off()

    def flash_to_sound(self, sound_file_path, update_every=0.01):
        sound = read(sound_file_path)
        sampling_rate = get_sample_rate(sound_file_path)

        sound = np.array(sound[1], dtype=float)
        mono = sound[:, 0] + sound[:, 1] / 2.0
        loudness = abs(mono) / abs(mono).max()

        # downsample by max pooling over update_every chunks
        remainder = int(loudness.shape[0] % (sampling_rate * update_every))
        loudness = loudness[0:-remainder]
        loudness = loudness.reshape(-1, int(sampling_rate * update_every))
        loudness = np.max(loudness, 1)

        # LEDs on if over a volume threshold
        for level in loudness:
            if level > 0.6:
                self.turn_on()
            else:
                self.turn_off()
            time.sleep(update_every)

        self.turn_off()

    def turn_on(self):
        for pin in self.led_pins:
            GPIO.output(pin, GPIO.HIGH)

    def turn_off(self):
        for pin in self.led_pins:
            GPIO.output(pin, GPIO.LOW)

    def wave(self, length):
        time.sleep(1)
        while 1:
            for pin in self.led_pins:
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(length)
            for pin in self.led_pins:
                GPIO.output(pin, GPIO.LOW)
                time.sleep(length)

    def pulse(self, pwm_pins, level, wait=0.01):
        for p in self.pwm_pins:
            p.start(0)
        while 1:
            for x in range(100):
                for p in self.pwm_pins:
                    p.ChangeDutyCycle(x)
                time.sleep(wait)

            for x in range(100, 0, -1):
                for p in self.pwm_pins:
                    p.ChangeDutyCycle(x)
                time.sleep(wait)

    def stop_pulse(self, pwm_pins, GPIO):
        for p in self.pwm_pins:
            p.stop()
        GPIO.cleanup()
