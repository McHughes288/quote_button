import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) # GPIO.BCM
ledPins = [7, 11, 12, 16, 29, 31]

for pin in ledPins:
    GPIO.setup(pin, GPIO.OUT)

# wave
for _ in range(4):
    for pin in ledPins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.1)
    for pin in ledPins:
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)

# flash
for _ in range(4):
    for pin in ledPins:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.6)
    for pin in ledPins:
        GPIO.output(pin, GPIO.LOW)
    time.sleep(0.6)


# dim up and down
pwm = [GPIO.PWM(pin, 100) for pin in ledPins]    # Created a PWM object

for p in pwm:
    p.start(0)                    # Started PWM at 0% duty cycle

try:
    while 1:                    # Loop will run forever
        for x in range(100):    # This Loop will run 100 times
            for p in pwm:
                p.ChangeDutyCycle(x) # Change duty cycle
            time.sleep(0.01)         # Delay of 10mS
            
        for x in range(100,0,-1): # Loop will run 100 times; 100 to 0
            for p in pwm:
                p.ChangeDutyCycle(x)
            time.sleep(0.01)
# If keyboard Interrupt (CTRL-C) is pressed
except KeyboardInterrupt:
    pass        # Go to next line
for p in pwm:
    p.stop()      # Stop the PWM
GPIO.cleanup()  # Make all the output pins LOW