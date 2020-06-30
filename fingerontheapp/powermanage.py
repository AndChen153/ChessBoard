import RPi.GPIO as GPIO
import time

channel = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

def powerToggle():
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(30)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(5)


    

while True:
    GPIO.output(channel, GPIO.LOW)
    print("off")
    for i in range(72)
        time.sleep(10)
        print("off")
    GPIO.output(channel, GPIO.HIGH)
    print("charge")
    for i in range(30)
        time.sleep(10)
        print("charge")
