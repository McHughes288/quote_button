import RPi.GPIO as GPIO
from raspberry.led import LEDArray
from raspberry.button import ButtonArray


class RaspberryPi:
    def __init__(self):

        button_names = ["Brian", "Mowbros", "Random", "Alert"]

        button_name_to_pin = {
            "Brian": 20,  # 38,
            "Mowbros": 12,  # 32,
            "Random": 21,  # 40,
            "Alert": 16,  # 36,
        }
        self.buttons = ButtonArray(button_names, button_name_to_pin)

        led_pins = [4, 17, 18, 23, 5, 6]  # [7, 11, 12, 16, 29, 31]
        led_pins = led_pins[::-1]
        self.leds = LEDArray(led_pins)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)  # BOARD)
        GPIO.setwarnings(False)

        self.buttons.setup()
        self.leds.setup()

    def terminate(self):
        self.leds.turn_off()
        GPIO.cleanup()
