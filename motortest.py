from time import sleep
import RPi.GPIO as GPIO

DIR1 = 21 # Directional GPIO Pin
STEP1 = 20 # Step GPIO Pin
DIR2 = 16 # Directional GPIO Pin
STEP2 = 12 # Step GPIO Pin
CW = GPIO.HIGH # CLockwise Rotation
CCW = GPIO.LOW # Counter Clockwise Rotation
LOW = GPIO.LOW
HIGH = GPIO.HIGH
SPR = 200  # Steps per Rotation (360/1.8)

GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)

GPIO.output(DIR1, CW)
GPIO.output(DIR2, CCW)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)


RESOLUTION = {'Full': (LOW, LOW, LOW),
              'Half': (HIGH, LOW, LOW),
              '1/4': (LOW, HIGH, LOW),
              '1/8': (HIGH, HIGH, LOW),
              '1/16': (LOW, LOW, HIGH),
              '1/32': (HIGH, LOW, HIGH)}

GPIO.output(MODE, RESOLUTION["Half"])

step_count = 200 * 32
delay = 0.0025 / 32

for x in range(step_count):
    GPIO.output(STEP1, GPIO.HIGH)
    GPIO.output(STEP2, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP1, GPIO.LOW)
    GPIO.output(STEP2, GPIO.LOW)
    sleep(delay)

sleep(1)
GPIO.output(DIR1, CCW)
GPIO.output(DIR2, CW)

for x in range(step_count):
    GPIO.output(STEP1, GPIO.HIGH)
    GPIO.output(STEP2, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP1, GPIO.LOW)
    GPIO.output(STEP2, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()
