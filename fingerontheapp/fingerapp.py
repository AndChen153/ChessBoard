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

# releases motors at the closing of the program
atexit.register(turnOffMotors)

stepstyles = [STEPPER.SINGLE, STEPPER.DOUBLE, STEPPER.INTERLEAVE, STEPPER.MICROSTEP]
#                   0               1                2                   3
stepDirection = [STEPPER.FORWARD, STEPPER.BACKWARD]
#                   0                      1


xPixels = 640 # how many pixels across x axis is on display
yPixels = 720 # how many pixels across y axis is on display
xSteps = 325 # how many steps across half of the x axis is on display
ySteps = 390 # how many steps across half of the  y axis is on display


# function to move stepper motors
# kit.stepper1 is the x axis motor and kit.stepper2 is the y axis motor
def stepper_worker(stepper, numsteps, direction, style):
    for i in range(numsteps):
        stepper.onestep(direction=direction, style=style)

# moves touch input in a square, most basic function
def squaremove():
    STEP=0
    x=0
    while x<3:
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
        
        x+=1
        #time.sleep(0.1)

# moves touchscreen stylus to a button and then back to the same spot
# this movement pattern was used to save time in coding since I only finished the image recognition program 2 days before the challenge started
def translation(xSteps, ySteps):

    for i in range(xSteps):
        kit.stepper1.onestep(direction=STEPPER.BACKWARD, style=STEPPER.DOUBLE)
    for i in range(ySteps):
        kit.stepper2.onestep(direction=STEPPER.BACKWARD, style=STEPPER.DOUBLE)
    for i in range(ySteps):
        kit.stepper2.onestep(direction=STEPPER.FORWARD , style=STEPPER.DOUBLE)
    for i in range(xSteps):
        kit.stepper1.onestep(direction=STEPPER.FORWARD , style=STEPPER.DOUBLE)

    turnOffMotors()



'''
if int(pixelCounts[0])>265:
        xdir = 1
    else:
        xdir = 0

    if int(pixelCounts[1])>265:
        ydir = 1
    else:
        ydir = 0
'''

'''while True:
    pixelInput = input('pixels?')
    pixelCounts = pixelInput.split(" ")

    
    #xdiff = abs(265-int(pixelCounts[0]))
    #ydiff = abs(265-int(pixelCounts[1]))

    xPercent = int(pixelCounts[0])/xPixels 
    yPercent = int(pixelCounts[1])/yPixels
    print (xPercent, yPercent)

    xNum = int(xPercent*xSteps)
    yNum = int(yPercent*ySteps)

    #translation(xNum, xdir, yNum, ydir)
    translation(xNum, yNum)
    while runNext == False:
        print("wait")
'''

while True:
    pixelInput = input('pixels?')
    pixelCounts = pixelInput.split(" ")

    # randomizing the amount of distance moved to hopefully throw off any detection of bots
    randomNumx = random.randint(0,30)
    randomNumy = random.randint(0,30)

    # subtract 100 because there is space on the sides of the video feed
    xPercent = (int(pixelCounts[0])-100)/xPixels 
    yPercent = int(pixelCounts[1])/yPixels    

    # convert the percentages from video feed into steps for the motors
    xNum = int(xPercent*xSteps)
    yNum = int(yPercent*ySteps)

    # subtract since the pen is not zeroed at the very corner
    # about 32 steps per block on an iphone 6s plus
    xNum -= 88
    yNum -= 100

    # setting bounds to prevent the pen from going off of the screen
    if xNum < 0:
        xNum = 0
    elif xNum < 30:
        xNum = 30
    elif xNum > 270:
        xNum = 270
    if yNum < 0:
        yNum = 0
    elif yNum < 30:
        yNum = 30
    elif yNum > 335:
        yNum = 335

    print (xPercent, yPercent, randomNumx, randomNumy)

    translation(xNum+randomNumx, yNum+randomNumy)