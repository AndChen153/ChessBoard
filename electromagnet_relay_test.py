import RPi.GPIO as GPIO
import time

channel = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


while True:
    y=input("a or b")

    if y == "a":
        GPIO.output(channel, GPIO.HIGH)
        

    elif y == "b":
        GPIO.output(channel, GPIO.LOW)

GPIO.cleanup()