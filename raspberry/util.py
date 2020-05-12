import wave
import mutagen.mp3

def get_sample_rate(sound_file_path):
    type_of_file = sound_file_path.split(".")[-1]

    if type_of_file == "mp3":
        mp3 = mutagen.mp3.MP3(sound_file_path)
        sampling_rate = mp3.info.sample_rate
    elif type_of_file == "wav":
        file_wav = wave.open(sound_file_path)
        sampling_rate = file_wav.getframerate()

    return sampling_rate


def flash_leds(led_pins, GPIO, repeat=4, length=0.6):
    for _ in range(repeat):
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(length)
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
        time.sleep(length)


def wave_leds(led_pins, GPIO, repeat=4, length=0.1):
    for _ in range(repeat):
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(length)
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(length)


def start_pwm(led_pins, GPIO):
    pwm_pins = [GPIO.PWM(pin, 100) for pin in led_pins]
    for p in pwm_pins:
        p.start(0)
    return pwm_pins


def dim_leds(pwm_pins, level):
    for p in pwm_pins:
        p.ChangeDutyCycle(level)
    time.sleep(0.01)


def stop_pwm(pwm_pins, GPIO):
    for p in pwm_pins:
        p.stop()
    GPIO.cleanup()