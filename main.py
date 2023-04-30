import keypad
import lcd
import time 
import notes
import speaker
import button
import RPi.GPIO as GPIO
from enum import Enum
from timeit import default_timer as timer
import numpy as np

class task:
    def __init__(self, state, period, elapsedTime, func):
        self.state = state
        self.period = period
        self.elapsedTime = elapsedTime
        self.func = func


class getKeyPadStates(Enum):
    startKey = 1
    getKey = 2
    changeOctaveDown = 3
    changeOctaveUp = 4
    changeRangeDown = 5
    changeRangeUp = 6

kpState = Enum('getKeyPadStates', ['startKey', 'getKey', 'waitKey', 'changeOctaveDown', 'changeOctaveUp', 'changeRangeDown', 'changeRangeUp'])

note = 40 # starting index of keyboard note
key = '' # key being pressed
timerStarted = 0
startTime = 0
endTime = 0

def KeyPad(state):
    global note
    global recordStart
    global key
    global timerStarted
    global startTime
    global endTime
    # transitions
    prevKey = key
    key = getKeyPadInput()
    if recordStart == 1:
        if timerStarted == 0:
            startTime = timer()
            timerStarted = 1
        if prevKey != key:
            endTime = timer()
            saveRecording(prevKey, startTime, endTime)
            startTime = timer()
    else:
        timerStarted = 0

    if state == kpState.startKey:
        state = kpState.waitKey
    elif state == kpState.getKey:
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
        if key != '':
            state = kpState.waitKey
        else: 
            state = kpState.getKey
    elif state == kpState.changeOctaveUp:
        if key != '':
            state = kpState.waitKey
        else: 
            state = kpState.getKey
    elif state == kpState.changeRangeDown:
        if key != '':
            state = kpState.waitKey
        else: 
            state = kpState.getKey
    elif state == kpState.changeRangeUp:
        if key != '':
            state = kpState.waitKey
        else: 
            state = kpState.getKey
    elif state == kpState.waitKey:
        if key == '':
            state = kpState.getKey
        else:
            state = kpState.waitKey
    else:
        state = kpState.getKey

    # state actions
    if state == kpState.startKey:
        state = kpState.getKey
    elif state == kpState.getKey:
        if key == '1':
            lcd.lcd_string("Key: " + str(notes.octave[note][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note][1])
        elif key == '2':
            lcd.lcd_string("Key: " + str(notes.octave[note+1][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+1][1])
        elif key == '3':
            lcd.lcd_string("Key: " + str(notes.octave[note+2][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+2][1])
        elif key == '4':
            lcd.lcd_string("Key: " + str(notes.octave[note+3][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+3][1])
        elif key == '5':
            lcd.lcd_string("Key: " + str(notes.octave[note+4][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+4][1])
        elif key == '6':
            lcd.lcd_string("Key: " + str(notes.octave[note+5][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+5][1])
        elif key == '7':
            lcd.lcd_string("Key: " + str(notes.octave[note+6][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+6][1])
        elif key == '8':
            lcd.lcd_string("Key: " + str(notes.octave[note+7][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+7][1])
        elif key == '9':
            lcd.lcd_string("Key: " + str(notes.octave[note+8][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+8][1])
        elif key == '*':
            lcd.lcd_string("Key: " + str(notes.octave[note+9][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+9][1])
        elif key == '0':
            lcd.lcd_string("Key: " + str(notes.octave[note+10][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+10][1])
        elif key == '#':
            lcd.lcd_string("Key: " + str(notes.octave[note+11][0]),lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+11][1])
        elif key == '':
            lcd.lcd_string("Key: ",lcd.LCD_LINE_1)
            if recordStart == 0:
                lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
            elif recordStart == 1:
                lcd.lcd_string("Recording",lcd.LCD_LINE_2)
            speaker.p.stop()
    elif state == kpState.changeOctaveDown:
        if note - 12 <= 0:
            note = 1
        else: 
            note -= 12
        print("new note: " + str(note))
        key = ''
    elif state == kpState.changeOctaveUp:
        if note + 12 >= 78:
            note = 77
        else:
            note += 12
        print("new note: " + str(note))
        key = ''
    elif state == kpState.changeRangeDown:
        if note - 1 <= 0:
            note = 1
        else:
            note -= 1
        print("new note: " + str(note))
        key = ''
    elif state == kpState.changeRangeUp:
        if note + 1 >= 78:
            note = 77
        else:
            note += 1
        print("new note: " + str(note))
        key = ''

    return state

def getKeyPadInput():
    key = ''
    key = keypad.readLine(keypad.L1, ["1","2","3","A"])
    if key != '':
        return key
    key = keypad.readLine(keypad.L2, ["4","5","6","B"])
    if key != '':
        return key
    key = keypad.readLine(keypad.L3, ["7","8","9","C"])
    if key != '':
        return key
    key = keypad.readLine(keypad.L4, ["*","0","#","D"])
    return key

recording = []

def saveRecording(prevKey, start, end):
    global recording
    global note

    freq = ''
    if prevKey == '1':
        freq = notes.octave[note][1]
    elif prevKey == '2':
        freq = notes.octave[note+1][1]
    elif prevKey == '3':
        freq = notes.octave[note+2][1]
    elif prevKey == '4':
        freq = notes.octave[note+3][1]
    elif prevKey == '5':
        freq = notes.octave[note+4][1]
    elif prevKey == '6':
        freq = notes.octave[note+5][1]
    elif prevKey == '7':
        freq = notes.octave[note+6][1]
    elif prevKey == '8':
        freq = notes.octave[note+7][1]
    elif prevKey == '9':
        freq = notes.octave[note+8][1]
    elif prevKey == '*':
        freq = notes.octave[note+9][1]
    elif prevKey == '0':
        freq = notes.octave[note+10][1]
    elif prevKey == '#':
        freq = notes.octave[note+11][1]
    else:
        freq = 0

    recording.append([freq, start, end])

        
class getRecStates(Enum):
    startRec = 1
    waitRec = 2
    releaseRec = 3
    waitStopRec = 4
    stopRecRelease = 5
    waitPlayback = 6
    releasePlayback = 7

recState = Enum('getRecStates', ['startRec', 'waitRec', 'releaseRec', 'waitStopRec', 'stopRecRelease', 'waitPlayback', 'releasePlayback'])

recordStart = 0

def Recording(state):
    global recordStart
    global recording
    # transitions
    if state == recState.startRec:
        state = recState.waitRec
    elif state == recState.waitRec:
        if GPIO.input(21) == 1:
            state = recState.releaseRec
        elif GPIO.input(16) == 1:
            state = recState.waitPlayback
        else:
            state = recState.waitRec
    elif state == recState.releaseRec:
        if GPIO.input(21) == 0:
            state = recState.waitStopRec
        else:
            state = recState.releaseRec
    elif state == recState.waitStopRec:
        if GPIO.input(20) == 1:
            state = recState.stopRecRelease
        else:
            state = recState.waitStopRec
    elif state == recState.stopRecRelease:
        if GPIO.input(20) == 0:
            state = recState.waitRec
        else:
            state = recState.stopRecRelease
    elif state == recState.waitPlayback:
        if GPIO.input(16) == 1:
            state = recState.waitPlayback
        else:
            state = recState.releasePlayback
    elif state == recState.releasePlayback:
        state = recState.waitRec
    
    # state actions
    if state == recState.startRec:
        recordStart = 0
    elif state == recState.waitRec:
        recordStart = 0
    elif state == recState.releaseRec:
        recordStart = 0
        recording.clear()
    elif state == recState.waitStopRec:
        recordStart = 1
    elif state == recState.stopRecRelease:
        recordStart = 1
    elif state == recState.waitPlayback:
        recordStart = 0
        lcd.lcd_string("Playback",lcd.LCD_LINE_1)
        lcd.lcd_string("",lcd.LCD_LINE_2)
        for x in range(len(recording)):
            print(recording[x])
            for y in np.arange(recording[x][1], recording[x][2], 0.1):
                print(y)
                if recording[x][0] != 0:
                    speaker.p.start(70)
                    speaker.p.ChangeFrequency(recording[x][0])
                else: 
                    speaker.p.stop()
                time.sleep(0.1)
        speaker.p.stop()



    return state


def main():
    # Initialise display
    lcd.lcd_start()
    lcd.lcd_string("Keyboard ready",lcd.LCD_LINE_1)
    keypad.keypad_start()

    try:
        state1 = kpState.startKey
        state2 = recState.startRec
        note = 40

        # state, period, elapsedTime, func
        # task1 = task(kpState.startKey, 0.1, 0.1, KeyPad)
        # task2 = task
        
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
            
            state1= KeyPad(state1)
            state2 = Recording(state2)

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
        speaker.p.stop()
        GPIO.cleanup()