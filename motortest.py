from time import sleep
import RPi.GPIO as GPIO

DIR = 21 # Directional GPIO Pin
STEP = 20 # Step GPIO Pin
CW = 1 # CLockwise Rotation
CCW = 2 # Counter Clockwise Rotation
SPR = 200  # Steps per Rotation (360/1.8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = SPR
delay = 0.005

for x in range(200):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(1)
GPIO.output(DIR, CCW)

for x in range(200):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()
