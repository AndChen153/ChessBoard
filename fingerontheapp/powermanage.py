import RPi.GPIO as GPIO
import time

channel = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

def powerToggle():
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(5)


while True:
    for i in range(4):
        powerToggle()
        time.sleep(355)
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(60)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(20)

