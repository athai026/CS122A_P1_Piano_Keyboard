import keypad
import lcd
import time 
import notes
import RPi.GPIO as GPIO
from enum import Enum

C1 = 26
C2 = 19
C3 = 13
C4 = 6

L1 = 5
L2 = 11
L3 = 9
L4 = 10

class task:
    def __init__(self, state, period, elapsedTime, func):
        self.state = state
        self.period = period
        self.elapsedTime = elapsedTime
        self.func = func

# note = 40


class getKeyPadStates(Enum):
    startKey = 1
    getKey = 2
    changeOctaveDown = 3
    changeOctaveUp = 4
    changeRangeDown = 5
    changeRangeUp = 6

kpState = Enum('getKeyPadStates', ['startKey', 'getKey', 'changeOctaveDown', 'changeOctaveUp', 'changeRangeDown', 'changeRangeUp'])

def KeyPad(state, note):
    # transitions
    key = ''
    if state == kpState.startKey:
        state = kpState.getKey
    elif state == kpState.getKey:
        key = getKeyPadInput()
        if key == 'A':
            state = kpState.changeRangeDown
        elif key == 'B':
            state = kpState.changeRangeUp
        elif key == 'C':
            state = kpState.changeOctaveDown
        elif key == 'D':
            state = kpState.changeOctaveUp
        else:
            state = kpState.getKey
    elif state == kpState.changeOctaveDown:
        state = kpState.getKey
    elif state == kpState.changeOctaveUp:
        state = kpState.getKey
    elif state == kpState.changeRangeDown:
        state = kpState.getKey
    elif state == kpState.changeRangeUp:
        state = kpState.getKey
    else:
        state = kpState.getKey

    # state actions
    if state == kpState.startKey:
        state = kpState.getKey
    elif state == kpState.getKey:
        if key == '1':
            lcd.lcd_string("Key: " + str(notes.octave[note][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note][1]),lcd.LCD_LINE_2)
        elif key == '2':
            lcd.lcd_string("Key: " + str(notes.octave[note+1][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+1][1]),lcd.LCD_LINE_2)
        elif key == '3':
            lcd.lcd_string("Key: " + str(notes.octave[note+2][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+2][1]),lcd.LCD_LINE_2)
        elif key == '4':
            lcd.lcd_string("Key: " + str(notes.octave[note+3][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+3][1]),lcd.LCD_LINE_2)
        elif key == '5':
            lcd.lcd_string("Key: " + str(notes.octave[note+4][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+4][1]),lcd.LCD_LINE_2)
        elif key == '6':
            lcd.lcd_string("Key: " + str(notes.octave[note+5][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+5][1]),lcd.LCD_LINE_2)
        elif key == '7':
            lcd.lcd_string("Key: " + str(notes.octave[note+6][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+6][1]),lcd.LCD_LINE_2)
        elif key == '8':
            lcd.lcd_string("Key: " + str(notes.octave[note+7][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+7][1]),lcd.LCD_LINE_2)
        elif key == '9':
            lcd.lcd_string("Key: " + str(notes.octave[note+8][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+8][1]),lcd.LCD_LINE_2)
        elif key == '*':
            lcd.lcd_string("Key: " + str(notes.octave[note+9][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+9][1]),lcd.LCD_LINE_2)
        elif key == '0':
            lcd.lcd_string("Key: " + str(notes.octave[note+10][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+10][1]),lcd.LCD_LINE_2)
        elif key == '#':
            lcd.lcd_string("Key: " + str(notes.octave[note+11][0]),lcd.LCD_LINE_1)
            lcd.lcd_string("Freq: " + str(notes.octave[note+11][1]),lcd.LCD_LINE_2) 
    elif state == kpState.changeOctaveDown:
        if note - 12 <= 0:
            note = 1
        else: 
            note -= 12
        print("new note: " + str(note))
        state = kpState.getKey
        key = ''
        # redo range
    elif state == kpState.changeOctaveUp:
        if note + 12 >= 78:
            note = 77
        else:
            note += 12
        print("new note: " + str(note))
        state = kpState.getKey
        key = ''
        # redo range
    elif state == kpState.changeRangeDown:
        if note - 1 <= 0:
            note = 1
        else:
            note -= 1
        print("new note: " + str(note))
        state = kpState.getKey
        key = ''
        #redo range
    elif state == kpState.changeRangeUp:
        if note + 1 >= 78:
            note = 77
        else:
            note += 1
        print("new note: " + str(note))
        state = kpState.getKey
        key = ''
        #redo range
    else:
        state = kpState.getKey

    return state, note

def getKeyPadInput():
    key = ''
    temp = ''
    while True:
        temp = keypad.readLine(keypad.L1, ["1","2","3","A"])
        if temp != '':
            break

        temp = keypad.readLine(keypad.L2, ["4","5","6","B"])
        if temp != '':
            break

        temp = keypad.readLine(keypad.L3, ["7","8","9","C"])
        if temp != '':
            break

        temp = keypad.readLine(keypad.L4, ["*","0","#","D"])
        if temp != '':
            break

        time.sleep(0.1)
    key = temp
    return key
        

def main():
    # Initialise display
    lcd.lcd_start()
    lcd.lcd_string("Application ready",lcd.LCD_LINE_1)
    
    try:
        state = kpState.startKey
        note = 40
        while True:
            # key = ''
            # temp = ''
            # temp = keypad.readLine(L1, ["1","2","3","A"])
            # if temp != '':
            #     print("key pressed: " + temp)
            # temp = keypad.readLine(L2, ["4","5","6","B"])
            # if temp != '':
            #     print("key pressed: " + temp)
            # temp = keypad.readLine(L3, ["7","8","9","C"])
            # if temp != '':
            #     print("key pressed: " + temp)
            # temp = keypad.readLine(L4, ["*","0","#","D"])
            # if temp != '':
            #     print("key pressed: " + temp)
            # time.sleep(0.1)
            
            state, note = KeyPad(state, note)
            time.sleep(0.2)
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