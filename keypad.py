#using code from https://maker.pro/raspberry-pi/tutorial/how-to-use-a-keypad-with-a-raspberry-pi-4
import RPi.GPIO as GPIO

C1 = 9
C2 = 10
C3 = 22
C4 = 27

L1 = 17
L2 = 4
L3 = 3
L4 = 2

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
        key = characters[0]
    elif(GPIO.input(C2) == 1):
        # print(characters[1])
        key = characters[1]
    elif(GPIO.input(C3) == 1):
        # print(characters[2])
        key = characters[2]
    elif(GPIO.input(C4) == 1):
        # print(characters[3])
        key = characters[3]
    else:
        key = ''
    GPIO.output(line, GPIO.LOW)
    return key
