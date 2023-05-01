#reference: https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import RPi.GPIO as GPIO
# import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(11, 400)
p1 = GPIO.PWM(13, 400)
# p.start(10)

# try:
#     p1.start(10)
#     print("10")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)
    
#     p1.start(20)
#     print("20")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(30)
#     print("30")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(40)
#     print("40")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(50)
#     print("50")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(60)
#     print("60")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(70)
#     print("70")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(80)
#     print("80")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(90)
#     print("90")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

#     p1.start(100)
#     print("100")
#     time.sleep(1)
#     p1.stop()
#     time.sleep(1)

# except KeyboardInterrupt:
#     pass

# p.stop()
# GPIO.cleanup()