#using code from https://maker.pro/raspberry-pi/tutorial/how-to-use-a-keypad-with-a-raspberry-pi-4
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

def keypad_start():
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
    key = ''
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        # print(characters[0])
        # lcd.lcd_string("Key pressed: " + characters[0],lcd.LCD_LINE_1)
        key = characters[0]
    elif(GPIO.input(C2) == 1):
        # print(characters[1])
        # lcd.lcd_string("Key pressed: " + characters[1],lcd.LCD_LINE_1)
        key = characters[1]
    elif(GPIO.input(C3) == 1):
        # print(characters[2])
        # lcd.lcd_string("Key pressed: " + characters[2],lcd.LCD_LINE_1)
        key = characters[2]
    elif(GPIO.input(C4) == 1):
        # print(characters[3])
        # lcd.lcd_string("Key pressed: " + characters[3],lcd.LCD_LINE_1)
        key = characters[3]
    else:
        key = ''
    GPIO.output(line, GPIO.LOW)
    return key
