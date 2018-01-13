import RPi.GPIO as GPIO
from time import sleep

class Button:
    def __init__(self, onPress):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(4, GPIO.BOTH, callback=onPress, bouncetime=200)

