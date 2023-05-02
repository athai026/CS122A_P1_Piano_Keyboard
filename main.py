import keypad
import lcd
import time 
import notes
import speaker
import button
import math
import RPi.GPIO as GPIO
from enum import Enum
from timeit import default_timer as timer
import numpy as np

############################## GLOBAL VARIABLES ##############################
numTasks = 3
period_gcd = 0.1
note = 40 # starting index of keyboard note
key = '' # key being pressed
timerStarted = False # check timer for recording
startTime = 0 # for recording
endTime = 0 # for recording
validPianoKeys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*', '#']
waitRelease = False # waiting for keypad release
recording = [[[]], [[]], [[]], [[]], [[]]]
numRecording = 0
recordStart = False # if recording
validPlaybackNum = False # if playback slot choice is valid
validPlaybackChoices = ['1', '2', '3', '4', '5']
waitingInput = False # waiting for input in Record task 
userPlaybackNum = '' # user input for playback num
inMenu = False # if user is in a menu, do not play metronome
metInput = '' # input for metronome
metPeriod = 0.1 # metronome period
validMetInput = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
getBPM = True
playTickCnt = 0
ticksPerPeriod = 0
tickCnt = 0
############################## GLOBAL VARIABLES ##############################


############################## TASK SCHEDULER CLASS ##############################
class task:
    def __init__(self, state, period, elapsedTime, func):
        self.state = state
        self.period = period
        self.elapsedTime = elapsedTime
        self.func = func
############################## TASK SCHEDULER CLASS ##############################


############################# PIANO TASK ##############################
class pianoStates(Enum):
    startKey = 1
    getKey = 2
    changeOctaveDown = 3
    changeOctaveUp = 4
    changeRangeDown = 5
    changeRangeUp = 6

pianoState = Enum('pianoStates', ['startKey', 'getKey', 'waitKey', 'changeOctaveDown', 'changeOctaveUp', 'changeRangeDown', 'changeRangeUp'])

def Piano(state):
    global note
    global recordStart
    global key
    global timerStarted
    global startTime
    global endTime
    global waitingInput
    global getBPM
    global waitRelease

    # if waiting for input in Recording or Metronom task, do not execute Piano task
    if getBPM or waitingInput:
        return state
    
    # check if key has change
    # if so, save previous key in recording (if recording)
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

    # transitions
    if state == pianoState.startKey:
        state = pianoState.waitKey
    elif state == pianoState.getKey:
        if key == 'A':
            state = pianoState.changeRangeDown
        elif key == 'B':
            state = pianoState.changeRangeUp
        elif key == 'C':
            state = pianoState.changeOctaveDown
        elif key == 'D':
            state = pianoState.changeOctaveUp
        else:
            state = pianoState.getKey
    elif state == pianoState.changeOctaveDown:
        if key != '':
            state = pianoState.waitKey
        else: 
            state = pianoState.getKey
    elif state == pianoState.changeOctaveUp:
        if key != '':
            state = pianoState.waitKey
        else: 
            state = pianoState.getKey
    elif state == pianoState.changeRangeDown:
        if key != '':
            state = pianoState.waitKey
        else: 
            state = pianoState.getKey
    elif state == pianoState.changeRangeUp:
        if key != '':
            state = pianoState.waitKey
        else: 
            state = pianoState.getKey
    elif state == pianoState.waitKey:
        if key == '':
            state = pianoState.getKey
        else:
            state = pianoState.waitKey
    else:
        state = pianoState.getKey

    # state actions
    if state == pianoState.startKey:
        state = pianoState.getKey
    elif state == pianoState.getKey:   
        waitRelease = False     
        if key in validPianoKeys:
            lcd.lcd_string("Key: " + str(notes.octave[note+notes.offsetLUT[key]][0]),lcd.LCD_LINE_1)
            printRecState()
            speaker.p.start(70)
            speaker.p.ChangeFrequency(notes.octave[note+notes.offsetLUT[key]][1])
        elif key == '':
            lcd.lcd_string("Key: ",lcd.LCD_LINE_1)
            printRecState()
            speaker.p.stop()
    elif state == pianoState.changeOctaveDown:
        if note - 12 <= 0:
            note = 1
        else: 
            note -= 12
        # print("new note: " + str(note))
        key = ''
    elif state == pianoState.changeOctaveUp:
        if note + 12 >= 78:
            note = 77
        else:
            note += 12
        # print("new note: " + str(note))
        key = ''
    elif state == pianoState.changeRangeDown:
        if note - 1 <= 0:
            note = 1
        else:
            note -= 1
        # print("new note: " + str(note))
        key = ''
    elif state == pianoState.changeRangeUp:
        if note + 1 >= 78:
            note = 77
        else:
            note += 1
        # print("new note: " + str(note))
        key = ''
    elif state == pianoState.waitKey:
        waitRelease = True

    return state
############################## PIANO TASK ##############################


############################## RECORD TASK ##############################
class recStates(Enum):
    startRec = 1
    waitRec = 2
    releaseRec = 3
    waitStopRec = 4
    releaseStopRec = 5
    releasePlayback = 6
    waitChoice = 7
    playPlayback = 8
    deleteRecordings = 9
    releaseDelete = 10
    confirmDelete = 11
    releaseDelete2 = 12

recState = Enum('recStates', ['startRec', 'waitRec', 'releaseRec', 'waitStopRec', 'releaseStopRec', 'releasePlayback', 'waitChoice', 'playPlayback', 'deleteRecordings', 'releaseDelete', 'confirmDelete', 'releaseDelete2'])

def Recording(state):
    global recordStart
    global recording
    global numRecording
    global validPlaybackNum
    global validPlaybackChoices
    global waitingInput
    global userPlaybackNum
    global getBPM
    global inMenu

    # if in metronome menu, do not execute Record task
    if getBPM:
        return state
    
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
        elif GPIO.input(16) == 1:
            state = recState.releaseDelete
        else:
            state = recState.waitChoice
    elif state == recState.playPlayback:
        state = recState.waitRec
    elif state == recState.releaseDelete:
        if GPIO.input(16) == 0:
            state = recState.confirmDelete
        else:
            state = recState.releaseDelete
    elif state == recState.confirmDelete:
        if GPIO.input(16) == 1:
            state = recState.releaseDelete2
        else:
            state = recState.confirmDelete
    elif state == recState.releaseDelete2:
        if GPIO.input(16) == 0:
            state = recState.deleteRecordings
        else:
            state = recState.releaseDelete2
    elif state == recState.deleteRecordings:
        state = recState.waitRec
    
    # state actions
    if state == recState.startRec:
        recordStart = False
        inMenu = False
    elif state == recState.waitRec:
        recordStart = False
        inMenu = False
    elif state == recState.releaseRec:
        recordStart = False
        inMenu = False
        numRecording = checkNumRecordings()
        recording[numRecording].clear()
    elif state == recState.waitStopRec:
        recordStart = True
        inMenu = False
    elif state == recState.releaseStopRec:
        recordStart = True
        inMenu = False
    elif state == recState.releasePlayback:
        recordStart = False
        inMenu = False
    elif state == recState.waitChoice:
        waitingInput = True
        inMenu = True
        if GPIO.input(5) == 1:
            waitingInput = False
            state = recState.waitRec
        lcd.lcd_string("Which recording?", lcd.LCD_LINE_1)
        lcd.lcd_string("1 2 3 4 5", lcd.LCD_LINE_2)
        userPlaybackNum = getKeyPadInput()
        if userPlaybackNum in validPlaybackChoices:
            validPlaybackNum = True
        elif userPlaybackNum != '':
            validPlaybackNum = False
            lcd.lcd_string("Invalid choice", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            time.sleep(1)
    elif state == recState.playPlayback:
        inMenu = True
        waitingInput = False
        validPlaybackNum = False
        recIndex = int(userPlaybackNum) - 1
        if not recording[recIndex][0]:
            lcd.lcd_string("Slot empty", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            time.sleep(1)
        else:
            lcd.lcd_string("Playback " + userPlaybackNum,lcd.LCD_LINE_1)
            lcd.lcd_string("",lcd.LCD_LINE_2)
            for x in range(len(recording[recIndex])):
                # print(recording[recIndex])
                for y in np.arange(recording[recIndex][x][1], recording[recIndex][x][2], 0.01):
                    # print(y)
                    if recording[recIndex][x][0] != 0:
                        speaker.p.start(70)
                        speaker.p.ChangeFrequency(recording[recIndex][x][0])
                    else: 
                        speaker.p.stop()
                    time.sleep(0.01)
            speaker.p.stop()
    elif state == recState.releaseDelete:
        waitingInput = True
        inMenu = True
    elif state == recState.confirmDelete:
        waitingInput = True
        inMenu = True
        if GPIO.input(5) == 1:
            waitingInput = False
            state = recState.waitRec
        lcd.lcd_string("Delete all", lcd.LCD_LINE_1)
        lcd.lcd_string("recordings?", lcd.LCD_LINE_2)
    elif state == recState.releaseDelete2:
        waitingInput = True
        inMenu = True
    elif state == recState.deleteRecordings:
        waitingInput = False
        inMenu = True
        for x in range(5):
            recording[x].clear()
            recording[x].append([])
        numRecording = 0
        lcd.lcd_string("All recordings", lcd.LCD_LINE_1)
        lcd.lcd_string("deleted", lcd.LCD_LINE_2)
        time.sleep(1)

    return state
############################## RECORD TASK ##############################


############################## METRONOME TASK ##############################
class metStates(Enum):
    startMet = 1
    getInput = 2
    releaseButton1 = 3
    setMet = 4
    releaseButton2 = 5
    playMet = 6
    noMet = 7

metState = Enum('metStates', ['startMet', 'getInput', 'releaseButton1', 'setMet', 'releaseButton2', 'playMet', 'noMet'])

def Metronome(state):
    global metInput
    global metPeriod
    global getBPM
    global playTickCnt
    global ticksPerPeriod
    global inMenu
    global waitRelease

    # transitions
    if state == metState.startMet:
        state = metState.getInput
    elif state == metState.getInput:
        if GPIO.input(26) == 1:
            state = metState.releaseButton1
        else:
            state = metState.getInput
    elif state == metState.releaseButton1:
        if GPIO.input(26) == 0:
            state = metState.setMet
        else:
            state = metState.releaseButton1
    elif state == metState.setMet:
        state = metState.playMet
    elif state == metState.releaseButton2:
        if GPIO.input(19) == 0:
            state = metState.getInput
        else:
            state = metState.releaseButton2
    elif state == metState.playMet:
        if not inMenu and GPIO.input(19) == 1:
            state = metState.releaseButton2
        else:
            state = metState.playMet
    elif state == metState.noMet:
        if not inMenu and GPIO.input(19) == 1:
            state = metState.releaseButton2
        else:
            state = metState.noMet

    # state actions
    if state == metState.startMet:
        getBPM = True
    elif state == metState.getInput:
        if GPIO.input(5) == 1:
            metInput = ''
        getBPM = True
        lcd.lcd_string("Enter BPM: ", lcd.LCD_LINE_1)
        input = getKeyPadInput()
        if input in validMetInput:
            metInput += input
        elif input != '':
            lcd.lcd_string("invalid input", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            time.sleep(1)
        lcd.lcd_string(metInput, lcd.LCD_LINE_2)
    elif state == metState.releaseButton1:
        getBPM = True
    elif state == metState.releaseButton2:
        getBPM = True
        metInput = ''
    elif state == metState.setMet:
        getBPM = False
        if metInput != '':
            ticksPerPeriod = math.floor(60 / metPeriod / float(metInput))
            # print(f"ticksPerPeriod = {ticksPerPeriod}")
        else: 
            state = metState.noMet
        playTickCnt = 0
    elif state == metState.playMet:
        getBPM = False
        if not inMenu and not waitRelease :
            if playTickCnt == ticksPerPeriod:
                speaker.p1.start(70)
                global tickCnt
                # print(f"tick {tickCnt}")
                tickCnt += 1
                time.sleep(0.01)
                speaker.p1.stop()
                playTickCnt = 0
            else:
                playTickCnt += 1

    return state
############################## METRONOME TASK ##############################


############################## HELPER FUNCTION ##############################
# used in Piano task -- prints recording state
def printRecState():
    global recordStart
    if recordStart == 0:
        lcd.lcd_string("Not recording",lcd.LCD_LINE_2)
    elif recordStart == 1:
        lcd.lcd_string("Recording",lcd.LCD_LINE_2)

# used in Piano, Record, Metronome task -- returns keypad input
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


# used in Piano task -- saves note played into recording
def saveRecording(prevKey, start, end):
    global recording
    global note
    global numRecording
    global validPianoKeys

    freq = ''
    
    if prevKey in validPianoKeys:
        freq = notes.octave[note+notes.offsetLUT[prevKey]][1]
    else:
        freq = 0

    recording[numRecording].append([freq, start, end])

# used in Record task -- check if all 5 recording slots are full
# if so, shift everything by one then record in 5th slot
def checkNumRecordings():
    global numRecording
    global recording

    if numRecording >= 5:
        # print("num recordings over 5")
        recording[0] = recording[1].copy()
        recording[1] = recording[2].copy()
        recording[2] = recording[3].copy()
        recording[3] = recording[4].copy()
        
        numRecording = 4

    return numRecording
############################## HELPER FUNCTION ##############################

def main():
    # Initialize display
    lcd.lcd_start()
    lcd.lcd_string("Keyboard ready",lcd.LCD_LINE_1)
    
    # Initialize keypad
    keypad.keypad_start()

    global numTasks
    global period_gcd
    global recording 
    global numRecording

    # reload recordings from previous run
    recording = np.load("savedRecordings.npy", allow_pickle=True)
    recording = recording.tolist()
    for record in recording:
        if len(record) > 1:
            numRecording += 1

    try:
        # initializing tasks
        task1 = task(metState.startMet, period_gcd, 0, Metronome)
        task2 = task(pianoState.startKey, period_gcd, 0, Piano)
        task3 = task(recState.startRec, period_gcd, 0, Recording)
        
        tasks = [task1, task2, task3]

        while True:
            interrupted = False
            for i in range(numTasks):
                if (tasks[i].elapsedTime >= tasks[i].period):
                    tasks[i].state = tasks[i].func(tasks[i].state)
                    tasks[i].elapsedTime = 0
                tasks[i].elapsedTime += period_gcd
                
                # kill switch
                if GPIO.input(12) == 1:
                    interrupted = True

            if interrupted:
                break
    except KeyboardInterrupt:
        # print("\nApplication stopped!")
        pass
    finally:
        np.save("savedRecordings.npy", np.array(recording, dtype=object)) # save recordings for next run
           
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_byte(0x01, lcd.LCD_CMD)
        lcd.lcd_string("Goodbye!",lcd.LCD_LINE_1)
        speaker.p.stop()
        speaker.p1.stop()
        GPIO.cleanup()