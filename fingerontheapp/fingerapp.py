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

# auto-disabling motors on shutdown
def turnOffMotors():
    kit.stepper1.release()
    kit.stepper2.release()

# create empty threads (these will hold the stepper 1 and 2 threads) so both motors can be ran at the same time
st1 = threading.Thread()
st2 = threading.Thread()

runNext = False

atexit.register(turnOffMotors)

stepstyles = [STEPPER.SINGLE, STEPPER.DOUBLE, STEPPER.INTERLEAVE, STEPPER.MICROSTEP]
#                   0               1                2                   3
stepDirection = [STEPPER.FORWARD, STEPPER.BACKWARD]
#                   0                      1
# so motors move same direction
stepDirectiony = [STEPPER.BACKWARD, STEPPER.FORWARD]
#                   0                      1

xPixels = 430 # how many pixels across x axis is on display
yPixels = 525 # how many pixels across y axis is on display
xSteps = 100 # how many steps across x axis is on display
ySteps = 100 # how many steps across y axis is on display

#REPLACE STEP VALUES BEFORE USE


def stepper_worker(stepper, numsteps, direction, style):
    # print("Steppin!")
    for _ in range(numsteps):
        stepper.onestep(direction=direction, style=style)
    # print("Done")

# moves touch input in a square, most basic function
def squaremove():
    STEP=0

    while True:
        if STEP == 0:
            print("300 forward")
            stepper_worker(kit.stepper1, 160, STEPPER.BACKWARD, stepstyles[1],)
            STEP = 1
        #time.sleep(0.1)

        if STEP == 1:
            print("250 forward")
            stepper_worker(kit.stepper2, 240, STEPPER.BACKWARD, stepstyles[1],)
            STEP = 2
        #time.sleep(0.1)
        
        if STEP == 2:
            print("300 back")
            stepper_worker(kit.stepper1, 160, STEPPER.FORWARD, stepstyles[1],)
            STEP = 3
        #time.sleep(0.1)

        if STEP == 3:
            print("250 back")
            stepper_worker(kit.stepper2, 240, STEPPER.FORWARD, stepstyles[1],)
            STEP = 0
        #time.sleep(0.1)

# moves in two directions and for differing x,y values 
def translation(xSteps, xDirection, ySteps, yDirection):
    global st1
    global st2
    global runNext
    runNext = False
    dirx = stepDirection[int(xDirection)]
    diry = stepDirectiony[int(yDirection)]

    # moving in a diagonal 
    if xSteps == ySteps:
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, xSteps, dirx, stepstyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, ySteps, diry, stepstyles[1],))
            st2.start()

    # un-diagonal movement, moves diagonal for equal x,y then completes remaining x or y steps in a straight line
    elif xSteps > ySteps:

        xTemp = xSteps - ySteps
        
        # diagonal movement
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, ySteps, dirx, stepstyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, ySteps, diry, stepstyles[1],))
            st2.start()

        # straight movement
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move x ")
            time.sleep(0.5)
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, xTemp, dirx, stepstyles[1],))
            st1.start()
            
    elif ySteps > xSteps:

        yTemp = ySteps-xSteps

        # diagonal movement
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, xSteps, dirx, stepstyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2,int(xSteps, diry, stepstyles[1],))
            st2.start()

        # straight movement
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move y ")
            time.sleep(0.5)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, yTemp, diry, stepstyles[1],))
            st2.start()    
    
    turnOffMotors()
    runNext = True

a=input("xSteps")
b=input("direction")
c=input("ySteps")
d=input("direction")

translation(int(a), int(b), int(c), int(d))
squaremove()

'''while True:
    pixelInput = input('pixels?')
    pixelCounts = pixelInput.split(" ")

    xPercent = pixelCounts[0]/xPixels 
    yPercent = pixelCounts[1]/yPixels

    xNum = xPercent*xSteps
    yNum = yPercent*ySteps

    translation(xNum, 1, yNum, 1)
    while runNext == False:
        wait=True
    translation(xNum, 0, yNum, 0)'''

