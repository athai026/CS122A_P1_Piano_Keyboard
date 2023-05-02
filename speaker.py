#reference: https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(11, 400) # piano and playback speaker
p1 = GPIO.PWM(13, 400) # metronome speaker