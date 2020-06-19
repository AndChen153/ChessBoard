import RPi.GPIO as GPIO

channel = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

y=input("a or b")

if y == "a":
    GPIO.output(channel, GPIO.HIGH)
    GPIO.cleanup()

elif y == "b":
    GPIO.output(channel, GPIO.LOW)
    GPIO.cleanup()