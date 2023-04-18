import keypad
import lcd
import time 
import RPi.GPIO as GPIO

C1 = 26
C2 = 19
C3 = 13
C4 = 6

L1 = 5
L2 = 11
L3 = 9
L4 = 10

def main():
    # Main program block
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(lcd.LCD_E, GPIO.OUT)  # E
    GPIO.setup(lcd.LCD_RS, GPIO.OUT) # RS
    GPIO.setup(lcd.LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(lcd.LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(lcd.LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(lcd.LCD_D7, GPIO.OUT) # DB7
 
    # Initialise display
    lcd.lcd_init()
    try:
        while True:
            keypad.readLine(L1, ["1","2","3","A"])
            keypad.readLine(L2, ["4","5","6","B"])
            keypad.readLine(L3, ["7","8","9","C"])
            keypad.readLine(L4, ["*","0","#","D"])
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_byte(0x01, lcd.LCD_CMD)
        lcd.lcd_string("Goodbye!",lcd.LCD_LINE_1)
        GPIO.cleanup()