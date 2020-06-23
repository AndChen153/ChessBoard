#!/usr/bin/python
#
# NOTE - Only for use on Raspberry Pi or other SBC.
#
import time
import atexit
import threading
import random
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

# create a default object, no changes to I2C address or frequency
kit = MotorKit()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    kit.stepper1.release()
    kit.stepper2.release()


atexit.register(turnOffMotors)

stepstyles = [STEPPER.SINGLE, STEPPER.DOUBLE, STEPPER.INTERLEAVE, STEPPER.MICROSTEP]


def stepper_worker(stepper, numsteps, direction, style):
    # print("Steppin!")
    for _ in range(numsteps):
        stepper.onestep(direction=direction, style=style)
    # print("Done")

STEP=0

while True:
    if STEP == 0:
        print("300 forward")
        stepper_worker(kit.stepper1, 230, STEPPER.FORWARD, stepstyles[1],)
        STEP = 1
    time.sleep(0.2)

    if STEP == 1:
        print("250 forward")
        stepper_worker(kit.stepper2, 300, STEPPER.FORWARD, stepstyles[1],)
        STEP = 2
    time.sleep(0.2)
    
    if STEP == 2:
        print("300 back")
        stepper_worker(kit.stepper1, 230, STEPPER.BACKWARD, stepstyles[1],)
        STEP = 3
    time.sleep(0.2)

    if STEP == 3:
        print("250 back")
        stepper_worker(kit.stepper2, 300, STEPPER.BACKWARD, stepstyles[1],)
        STEP = 0
    time.sleep(0.2)
