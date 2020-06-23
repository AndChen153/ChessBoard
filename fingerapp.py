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

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()  # pylint: disable=bad-thread-instantiation
st2 = threading.Thread()  # pylint: disable=bad-thread-instantiation


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
    if not st1.isAlive() and not st2.isAlive() and STEP == 0:
        print("300 forward")
        st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, 300, STEPPER.FORWARD, stepstyles[0],))
        st1.start()
        STEP = 1

    if not st2.isAlive() and not st1.isAlive() and STEP == 1:
        print("250 forward")
        st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, 250, STEPPER.FORWARD, stepstyles[0],))
        st2.start()
        STEP = 2
    
    if not st1.isAlive() and not st2.isAlive() and STEP == 2:
        print("300 back")
        st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, 300, STEPPER.BACKWARD, stepstyles[0],))
        st1.start()
        STEP = 3

    if not st2.isAlive() and not st2.isAlive() and STEP == 3:
        print("250 back")
        st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, 250, STEPPER.BACKWARD, stepstyles[0],))
        st2.start()
        STEP = 0

    time.sleep(0.1)  # Small delay to stop from constantly polling threads
    # see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733