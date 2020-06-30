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
#st1 = threading.Thread()
#st2 = threading.Thread()

runNext = False

atexit.register(turnOffMotors)

stepstyles = [STEPPER.SINGLE, STEPPER.DOUBLE, STEPPER.INTERLEAVE, STEPPER.MICROSTEP]
#                   0               1                2                   3
stepDirection = [STEPPER.FORWARD, STEPPER.BACKWARD]
#                   0                      1

'''
xPixels = 430 # how many pixels across x axis is on display
yPixels = 530 # how many pixels across y axis is on display
xSteps = 180 # how many steps across half of the x axis is on display
ySteps = 260 # how many steps across half of the  y axis is on display
'''


xPixels = 430 # how many pixels across x axis is on display
yPixels = 530 # how many pixels across y axis is on display
xSteps = 325 # how many steps across half of the x axis is on display
ySteps = 390 # how many steps across half of the  y axis is on display



def stepper_worker(stepper, numsteps, direction, style):
    # print("Steppin!")
    for i in range(numsteps):
        stepper.onestep(direction=direction, style=style)
    # print("Done")

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

# moves in two directions and for differing x,y values 
def translation(xSteps, ySteps):
    global runNext
    #dirx = stepDirection[int(xdir)]
    #diry = stepDirection[int(ydir)]
    '''if int(xdir) == 1:
        dirx2 = stepDirection[0]
    else:
        dirx2 = stepDirection[1]
    if int(ydir) == 1:
        diry2 = stepDirection[0]
    else:
        diry2 = stepDirection[1]'''

    for i in range(xSteps):
        kit.stepper1.onestep(direction=STEPPER.BACKWARD, style=STEPPER.DOUBLE)
    for i in range(ySteps):
        kit.stepper2.onestep(direction=STEPPER.BACKWARD, style=STEPPER.DOUBLE)
    for i in range(ySteps):
        kit.stepper2.onestep(direction=STEPPER.FORWARD , style=STEPPER.DOUBLE)
    for i in range(xSteps):
        kit.stepper1.onestep(direction=STEPPER.FORWARD , style=STEPPER.DOUBLE)

    turnOffMotors()
    runNext = True

#squaremove()

'''while True:
    pixelInput = input('pixels?')
    pixelCounts = pixelInput.split(" ")
    
    '''if int(pixelCounts[0])>265:
        xdir = 1
    else:
        xdir = 0

    if int(pixelCounts[1])>265:
        ydir = 1
    else:
        ydir = 0'''
    
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
        print("wait")'''

while True:
    pixelInput = input('pixels?')
    pixelCounts = pixelInput.split(" ")
    
    '''if int(pixelCounts[0])>265:
        xdir = 1
    else:
        xdir = 0

    if int(pixelCounts[1])>265:
        ydir = 1
    else:
        ydir = 0'''
    
    #xdiff = abs(265-int(pixelCounts[0]))
    #ydiff = abs(265-int(pixelCounts[1]))

    xPercent = (int(pixelCounts[0])-100)/xPixels 
    yPercent = int(pixelCounts[1])/yPixels
    print (xPercent, yPercent)

    xNum = int(xPercent*xSteps)
    yNum = int(yPercent*ySteps)
    xNum -= 90
    yNum -= 90

    #translation(xNum, xdir, yNum, ydir)
    translation(xNum, yNum)
    while runNext == False:
        print("wait")
