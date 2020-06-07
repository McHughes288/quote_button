import RPi.GPIO as GPIO
from raspberry.led import LEDArray
from raspberry.button import ButtonArray


class RaspberryPi:
    def __init__(self):

        button_names = ["TV", "Films", "Memes", "recordings"]

        button_name_to_pin = {
            "TV": 20,
            "Films": 12,
            "recordings": 21,
            "Memes": 16,
        }
        self.buttons = ButtonArray(button_names, button_name_to_pin)

        led_pins = [4, 17, 18, 23, 5, 6]
        led_pins = led_pins[::-1]
        self.leds = LEDArray(led_pins)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.buttons.setup()
        self.leds.setup()

    def terminate(self):
        self.leds.turn_off()
        GPIO.cleanup()

class RaspberryPiZero:
    def __init__(self):

        button_names = ["Sounds"]
        button_name_to_pin = {"Sounds": 23}
        self.buttons = ButtonArray(button_names, button_name_to_pin)

        led_pins = [26]
        self.leds = LEDArray(led_pins)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.buttons.setup()
        self.leds.setup()

    def terminate(self):
        self.leds.turn_off()
        GPIO.cleanup()
