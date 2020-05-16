import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time


class LCDScreen:
    def __init__(self, waiting_message="WAITING", lcd_columns=16, lcd_rows=2):

        # Raspberry Pi Pin Config:
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D19)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d6 = digitalio.DigitalInOut(board.D22)
        lcd_d7 = digitalio.DigitalInOut(board.D27)
        lcd_backlight = digitalio.DigitalInOut(board.D4)

        # Initialise the lcd class
        print("Initialising LCD...")
        self.lcd = characterlcd.Character_LCD_Mono(
            lcd_rs,
            lcd_en,
            lcd_d4,
            lcd_d5,
            lcd_d6,
            lcd_d7,
            lcd_columns,
            lcd_rows,
            lcd_backlight,
        )

        self.lcd_columns = lcd_columns
        self.lcd_rows = lcd_rows

        self.waiting_message = waiting_message

        self.turn_on()
        self.display("BRESS ME\nPLEASE SIR")

    def turn_on(self):
        self.lcd.clear()
        self.lcd.backlight = True

    def turn_off(self):
        self.lcd.clear()
        self.lcd.backlight = False

    def display(self, message, print_to_console=True):
        if print_to_console:
            print(message)
        self.lcd.clear()
        self.lcd.message = message

    def scroll(self, message, repeat=2):
        self.display(message)
        if len(message) > self.lcd_columns:
            for _ in range(repeat):
                time.sleep(2)
                for i in range(len(message) - self.lcd_columns):
                    self.lcd.move_left()
                    time.sleep(0.2)

                time.sleep(1)
                self.display(message, print_to_console=False)
        else:
            time.sleep(4)

        time.sleep(2)
        self.display(self.waiting_message)
