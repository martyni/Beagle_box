import Adafruit_BBIO.GPIO as GPIO
from time import sleep

topButton = "P9_11"
bottomButton = "P9_13"

GPIO.setup(topButton, GPIO.IN)
GPIO.setup(bottomButton, GPIO.IN)

while True:
    if GPIO.input(topButton):
        print("top button on")
    if GPIO.input(bottomButton):
        print("bottom button on")
