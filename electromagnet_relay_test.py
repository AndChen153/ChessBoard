import RPi.GPIO as GPIO
import time

channel = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

y=input("a or b")

if y == "a":
    GPIO.output(channel, GPIO.HIGH)

elif y == "b":
    GPIO.output(channel, GPIO.LOW)