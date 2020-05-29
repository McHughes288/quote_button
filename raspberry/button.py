import RPi.GPIO as GPIO

class ButtonArray:
    def __init__(self, names, name_to_pin):
        self.names = names
        self.name_to_pin = name_to_pin
    
    def setup(self):
        # button pins
        for pin in self.name_to_pin.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def pressed(self, name):
        button_pin = self.name_to_pin[name]
        return GPIO.input(button_pin) == GPIO.LOW