import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # playback & delete playback button
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # stop recording button
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # start recording button
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # back out of playback menu & delete BPM input button
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # confirm BPM button
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # re-enter BPM button
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # kill program button
