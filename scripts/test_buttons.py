import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

button_pin_list = [32, 36, 38, 40]

for button in button_pin_list:
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:  # Run forever
    for button in button_pin_list:
        if GPIO.input(button) == GPIO.LOW:
            print(f"Button {button} was pushed!")
