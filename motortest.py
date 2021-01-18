from time import sleep
import RPi.GPIO as GPIO

DIR = 21 # Directional GPIO Pin
STEP = 20 # Step GPIO Pin
CW = GPIO.HIGH # CLockwise Rotation
CCW = GPIO.LOW # Counter Clockwise Rotation
LOW = GPIO.LOW
HIGH = GPIO.HIGH
SPR = 200  # Steps per Rotation (360/1.8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)

RESOLUTION = {'Full': (LOW, LOW, LOW),
              'Half': (HIGH, LOW, LOW),
              '1/4': (LOW, HIGH, LOW),
              '1/8': (HIGH, HIGH, LOW),
              '1/16': (LOW, LOW, HIGH),
              '1/32': (HIGH, LOW, HIGH)}

GPIO.output(MODE, RESOLUTION["1/32"])

step_count = 200 * 32
delay = 0.0025 / 32

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(1)
GPIO.output(DIR, CCW)

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()
