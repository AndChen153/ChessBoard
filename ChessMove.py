

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
import random
import sys

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads) so both motors can be ran at the same time
st1 = threading.Thread()    #x axis
st2 = threading.Thread()    #y axis


XAxisStepper = mh.getStepper(200, 1)      # 200 steps/rev (1.8 degrees per step), motor port #1
YAxisStepper = mh.getStepper(200, 2)      # 200 steps/rev (1.8 degrees per step), motor port #2
XAxisStepper.setSpeed(60)
YAxisStepper.setSpeed(60)


stepStyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3
stepDirection = [Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.BACKWARD]
#                   0                               1

#number of steps per spaces on the chessboard
steps=150

# turns off motors at exit of program
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

#runs motors
def stepper_worker(stepper, numsteps, direction, style):
    print("Steppin!")
    stepper.step(numsteps, direction, style)
    print("Done \n")

#to prevent weird motor movements (stops moving halfway) while only moving one motor
def jiggle(stepper):
    if stepper == "x":
        if st1.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 5, stepDirection[0], stepStyles[2],))
            st2.start()
        if st1.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 5, stepDirection[1], stepStyles[2],))
            st2.start()

    elif stepper == "y":
        if st2.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 5, stepDirection[0], stepStyles[2],))
            st1.start()
        if st2.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 5, stepDirection[1], stepStyles[2],))
            st1.start()

#direction -> 0 is forward 1 is backward
def translation(xPlaces, xDirection, yPlaces, yDirection):
    xPlaces = int(xPlaces)*steps
    yPlaces = int(yPlaces)*steps
    dirx = stepDirection[int(xDirection)]
    diry = stepDirection[int(yDirection)]

    #moving in a diagonal
    if xPlaces == yPlaces:
        if not st1.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xPlaces, dirx, stepStyles[2],))
            st1.start()
        if not st2.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yPlaces, diry, stepStyles[2],))
            st2.start()

    #un-diagonal movement
    elif xPlaces > yPlaces:
        xTemp = xPlaces - yPlaces
        #diagonal
        if not st1.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, yPlaces, dirx, stepStyles[2],))
            st1.start()
        if not st2.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yPlaces, diry, stepStyles[2],))
            st2.start()
        #straight
        if not st1.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xTemp, dirx, stepStyles[2],))
            st1.start()
        if st1.isAlive():
            jiggle("y")
    
    elif yPlaces > xPlaces:
        yTemp = yPlaces-xPlaces
        #diagonal
        if not st1.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xPlaces, dirx, stepStyles[2],))
            st1.start()
        if not st2.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper,xPlaces, diry, stepStyles[2],))
            st2.start()
        #straight
        if not st2.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yTemp, diry, stepStyles[2],))
            st2.start()
        if st1.isAlive():
            jiggle("x")

    turnOffMotors()

#sys.argv=(xPlaces, xDirection, yPlaces, yDirection)
#            0          1           2          3
translation(sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3])


st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 300, stepDirection[1], stepStyles[2],))
st1.start()
jiggle("x")

'''
if not st1.isAlive():
    st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(x), dirx, stepStyles[2],))
    st1.start()
if not st2.isAlive():
    st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, int(y), diry, stepStyles[2],))
    st2.start()
'''