import wave
import mutagen.mp3
import time


def get_sample_rate(sound_file_path):
    type_of_file = sound_file_path.split(".")[-1]

    if type_of_file == "mp3":
        mp3 = mutagen.mp3.MP3(sound_file_path)
        sampling_rate = mp3.info.sample_rate
    elif type_of_file == "wav":
        file_wav = wave.open(sound_file_path)
        sampling_rate = file_wav.getframerate()

    return sampling_rate


def start_pwm(led_pins, GPIO):
    pwm_pins = [GPIO.PWM(pin, 100) for pin in led_pins]
    for p in pwm_pins:
        p.start(0)
    return pwm_pins


def dim_leds(pwm_pins, level, wait=0.01):
    for p in pwm_pins:
        p.ChangeDutyCycle(level)
    time.sleep(wait)


def stop_pwm(pwm_pins, GPIO):
    for p in pwm_pins:
        p.stop()
    GPIO.cleanup()
