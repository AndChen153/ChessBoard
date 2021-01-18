from time import sleep
import RPi.GPIO as GPIO

DIR = 3 # Directional GPIO Pin
STEP = 2 # Step GPIO Pin
CW = 1 # CLockwise Rotation
CCW = 2 # Counter Clockwise Rotation
SPR = 200  # Steps per Rotation (360/1.8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR,CW)

step_count = SPR
delay = 0.005

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()