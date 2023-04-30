import RPi.GPIO as GPIO
import time
import notes

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
p = GPIO.PWM(16, 10)
# p.start(70)
# for x in range(40, 53):
#     p.ChangeFrequency(notes.octave[x][1])
#     print(x)
#     time.sleep(1)

# for dc in range(0, 101, 5):
#     p.ChangeDutyCycle(dc)
#     print(dc)
#     time.sleep(0.5)
# p.stop()
# GPIO.cleanup()