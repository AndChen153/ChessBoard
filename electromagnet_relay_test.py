import RPi.GPIO as GPIO
import time

channel = 23
channel2 = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
GPIO.setup(channel2, GPIO.OUT)


while True:
    y=input("a or b or c or d")

    if y == "a":
        GPIO.output(channel, GPIO.HIGH)
        

    elif y == "b":
        GPIO.output(channel, GPIO.LOW)

    elif y == "c":
        GPIO.output(channel2, GPIO.HIGH)

    elif y == "d":
        GPIO.output(channel2, GPIO.LOW)

GPIO.cleanup()



