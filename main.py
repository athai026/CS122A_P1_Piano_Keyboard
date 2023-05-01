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
timerStarted = False
startTime = 0
endTime = 0

def Piano(state):
    global note
    global recordStart
    global key
    global timerStarted
    global startTime
    global endTime
    global waitingInput
    # transitions
    prevKey = key
    key = getKeyPadInput()
    if recordStart:
        if not timerStarted:
            startTime = timer()
            timerStarted = True
        if prevKey != key:
            endTime = timer()
            saveRecording(prevKey, startTime, endTime)
            startTime = timer()
    else:
        timerStarted = False

    if state == kpState.startKey:
        state = kpState.waitKey
    elif state == kpState.getKey:
        if not waitingInput:
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
        if not waitingInput:
            if key == '1':
                lcd.lcd_string("Key: " + str(notes.octave[note][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note][1])
            elif key == '2':
                lcd.lcd_string("Key: " + str(notes.octave[note+1][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+1][1])
            elif key == '3':
                lcd.lcd_string("Key: " + str(notes.octave[note+2][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+2][1])
            elif key == '4':
                lcd.lcd_string("Key: " + str(notes.octave[note+3][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+3][1])
            elif key == '5':
                lcd.lcd_string("Key: " + str(notes.octave[note+4][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+4][1])
            elif key == '6':
                lcd.lcd_string("Key: " + str(notes.octave[note+5][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+5][1])
            elif key == '7':
                lcd.lcd_string("Key: " + str(notes.octave[note+6][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+6][1])
            elif key == '8':
                lcd.lcd_string("Key: " + str(notes.octave[note+7][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+7][1])
            elif key == '9':
                lcd.lcd_string("Key: " + str(notes.octave[note+8][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+8][1])
            elif key == '*':
                lcd.lcd_string("Key: " + str(notes.octave[note+9][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+9][1])
            elif key == '0':
                lcd.lcd_string("Key: " + str(notes.octave[note+10][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+10][1])
            elif key == '#':
                lcd.lcd_string("Key: " + str(notes.octave[note+11][0]),lcd.LCD_LINE_1)
                printRecState()
                speaker.p.start(70)
                speaker.p.ChangeFrequency(notes.octave[note+11][1])
            elif key == '':
                lcd.lcd_string("Key: ",lcd.LCD_LINE_1)
                printRecState()
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

def printRecState():
    global recordStart
    if recordStart == 0:
        lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
    elif recordStart == 1:
        lcd.lcd_string("Recording",lcd.LCD_LINE_2)

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

recording = [[[]], [[]], [[]], [[]], [[]]]
numRecording = 0

def saveRecording(prevKey, start, end):
    global recording
    global note
    global numRecording
    # numRecording = checkNumRecordings()

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

    recording[numRecording].append([freq, start, end])

def checkNumRecordings():
    global numRecording
    global recording

    if numRecording >= 5:
        print("num recordings over 5")
        recording[0] = recording[1].copy()
        recording[1] = recording[2].copy()
        recording[2] = recording[3].copy()
        recording[3] = recording[4].copy()
        # recording[4].clear()
        
        numRecording = 4

    return numRecording
        
class getRecStates(Enum):
    startRec = 1
    waitRec = 2
    releaseRec = 3
    waitStopRec = 4
    releaseStopRec = 5
    releasePlayback = 6
    waitChoice = 7
    playPlayback = 8

recState = Enum('getRecStates', ['startRec', 'waitRec', 'releaseRec', 'waitStopRec', 'releaseStopRec', 'releasePlayback', 'waitChoice', 'playPlayback'])

recordStart = False
validPlaybackNum = False
validPlaybackChoices = ['1', '2', '3', '4', '5']
waitingInput = False
userChoice = ''

def Recording(state):
    global recordStart
    global recording
    global numRecording
    global validPlaybackNum
    global validPlaybackChoices
    global waitingInput
    global userChoice
    # transitions
    if state == recState.startRec:
        state = recState.waitRec
    elif state == recState.waitRec:
        if GPIO.input(21) == 1:
            state = recState.releaseRec
        elif GPIO.input(16) == 1:
            state = recState.releasePlayback
        else:
            state = recState.waitRec
    elif state == recState.releaseRec:
        if GPIO.input(21) == 0:
            state = recState.waitStopRec
        else:
            state = recState.releaseRec
    elif state == recState.waitStopRec:
        if GPIO.input(20) == 1:
            state = recState.releaseStopRec
        else:
            state = recState.waitStopRec
    elif state == recState.releaseStopRec:
        if GPIO.input(20) == 0:
            state = recState.waitRec
            numRecording += 1
        else:
            state = recState.releaseStopRec
    elif state == recState.releasePlayback:
        if GPIO.input(16) == 0:
            state = recState.waitChoice
        else:
            state = recState.releasePlayback
    elif state == recState.waitChoice:
        if validPlaybackNum:
            state = recState.playPlayback
        else:
            state = recState.waitChoice
    elif state == recState.playPlayback:
        state = recState.waitRec
    
    # state actions
    if state == recState.startRec:
        recordStart = False
    elif state == recState.waitRec:
        recordStart = False
    elif state == recState.releaseRec:
        recordStart = False
        numRecording = checkNumRecordings()
        recording[numRecording].clear()
    elif state == recState.waitStopRec:
        recordStart = True
    elif state == recState.releaseStopRec:
        recordStart = True
    elif state == recState.releasePlayback:
        recordStart = False
    elif state == recState.waitChoice:
        waitingInput = True
        if GPIO.input(5) == 1:
            waitingInput = False
            state = recState.waitRec
        lcd.lcd_string("Which recording?", lcd.LCD_LINE_1)
        lcd.lcd_string("1 2 3 4 5", lcd.LCD_LINE_2)
        userChoice = getKeyPadInput()
        if userChoice in validPlaybackChoices:
            validPlaybackNum = True
        elif userChoice != '':
            validPlaybackNum = False
            lcd.lcd_string("Invalid choice", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            time.sleep(1)
    elif state == recState.playPlayback:
        waitingInput = False
        validPlaybackNum = False
        recIndex = int(userChoice) - 1
        if not recording[recIndex][0]:
            lcd.lcd_string("Slot empty", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            time.sleep(1)
        else:
            lcd.lcd_string("Playback " + userChoice,lcd.LCD_LINE_1)
            lcd.lcd_string("",lcd.LCD_LINE_2)
            for x in range(len(recording[recIndex])):
                print(recording[recIndex])
                for y in np.arange(recording[recIndex][x][1], recording[recIndex][x][2], 0.01):
                    print(y)
                    if recording[recIndex][x][0] != 0:
                        speaker.p.start(70)
                        speaker.p.ChangeFrequency(recording[recIndex][x][0])
                    else: 
                        speaker.p.stop()
                    time.sleep(0.01)
            speaker.p.stop()

    return state

numTasks = 2
period_gcd = 0.01

def main():
    # Initialise display
    lcd.lcd_start()
    lcd.lcd_string("Keyboard ready",lcd.LCD_LINE_1)
    keypad.keypad_start()

    global numTasks
    global period_gcd

    try:
        # state, period, elapsedTime, func
        task1 = task(kpState.startKey, 0.01, 0, Piano)
        task2 = task(recState.startRec, 0.01, 0, Recording)
        
        tasks = [task1, task2]

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
            # time.sleep(0.01)
            
            # state1= Piano(state1)
            # state2 = Recording(state2)

            for i in range(numTasks):
                if (tasks[i].elapsedTime >= tasks[i].period):
                    tasks[i].state = tasks[i].func(tasks[i].state)
                    tasks[i].elapsedTime = 0
                tasks[i].elapsedTime += period_gcd

            time.sleep(period_gcd)
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