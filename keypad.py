import RPi.GPIO as GPIO
import time

import lcd

C1 = 26
C2 = 19
C3 = 13
C4 = 6

L1 = 5
L2 = 11
L3 = 9
L4 = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
        lcd.lcd_string(characters[0],lcd.LCD_LINE_1)
    if(GPIO.input(C2) == 1):
        print(characters[1])
        lcd.lcd_string(characters[1],lcd.LCD_LINE_1)
    if(GPIO.input(C3) == 1):
        print(characters[2])
        lcd.lcd_string(characters[2],lcd.LCD_LINE_1)
    if(GPIO.input(C4) == 1):
        print(characters[3])
        lcd.lcd_string(characters[3],lcd.LCD_LINE_1)
    GPIO.output(line, GPIO.LOW)

def main():
    try:
        while True:
            readLine(L1, ["1","2","3","A"])
            readLine(L2, ["4","5","6","B"])
            readLine(L3, ["7","8","9","C"])
            readLine(L4, ["*","0","#","D"])
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
 
if __name__ == '__main__':
    main()
