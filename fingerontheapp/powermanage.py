# program to charge the touch pen at intervals to prevent a behavior of charing to full then turning off
# pen i used https://www.wiwu.com/product-page/p666-wiwu-active-stylus-pen

import RPi.GPIO as GPIO
import time

# assigning a gpio channel to control a relay that is connected to a spliced micro usb cable
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
    for i in range(72):
        time.sleep(10)
        print("off")
    GPIO.output(channel, GPIO.HIGH)
    print("charge")
    for i in range(30):
        time.sleep(10)
        print("charge")
