import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time


class LCDScreen:
    def __init__(self, lcd_columns=16, lcd_rows=2):

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
            lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
        )
        
        self.turn_on()
        self.display("STARTING\nUP!")
    
    def turn_on(self):
        self.lcd.clear()
        self.lcd.backlight = True

    def turn_off(self):
        self.lcd.clear()
        self.lcd.backlight = False

    def display(self, message, clear=True, scroll=False, t=None, blink=False):
        print(message)
        if self.lcd is not None:
            if clear:
                self.lcd.clear()
            self.lcd.blink = blink
            self.lcd.message = message
            if scroll:
                for i in range(len(message)):
                    time.sleep(0.2)
                    self.lcd.move_left()
                self.lcd.clear()
                self.lcd.message = message
            if t:
                time.sleep(t)


    