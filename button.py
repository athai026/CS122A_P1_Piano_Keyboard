import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



# def topButton_callback(channel):
#     print("top button WAS pushed")

# def bottomButton_callback(channel):
#     print("bottom button WAS pushed")

# GPIO.add_event_detect(20, GPIO.RISING, callback=topButton_callback)
# GPIO.add_event_detect(21, GPIO.RISING, callback=bottomButton_callback)

# while True: 
#     if GPIO.input(16) == 1:
#         print("top button pushed")
#     if GPIO.input(20) == 1:
#         print("middle button pushed")
#     if GPIO.input(21) == 1:
#         print("bottom button pushed")
#     time.sleep(0.1)

# message = input("Press enter to quit\n\n")

# GPIO.cleanup()