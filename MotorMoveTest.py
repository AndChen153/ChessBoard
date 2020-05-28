#to find the number of steps for each square on the chessboard

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
import random

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()

# turns off motors at exit of program
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

XAxisStepper = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
YAxisStepper = mh.getStepper(200, 2)      # 200 steps/rev, motor port #2
XAxisStepper.setSpeed(60)
YAxisStepper.setSpeed(60)

stepStyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3

stepDirection = [Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.BACKWARD]
#                   0                               1

def stepper_worker(stepper, numsteps, direction, style):
    print("Steppin!")
    stepper.step(numsteps, direction, style)
    print("Done \n")

#both motors have to be moving at the same time to eliminate the weird motor stopping issue

while (True):
    x=input("X steps? \n")
    directionx = input("direction? \n")
    dirx=stepDirection[int(directionx)]

    y=input("y steps? \n")
    directiony = input("direction? \n")
    diry=stepDirection[int(directiony)]

    if not st1.isAlive():
        st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(x), dirx, stepStyles[2],))
        st1.start()
    if not st2.isAlive():
        st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, int(y), diry, stepStyles[2],))
        st2.start()

    time.sleep(0.1)
    #turnOffMotors()



    '''
    YAxisStepper.step(600, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    XAxisStepper.step(600, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    time.sleep (0.1)
    XAxisStepper.step(600, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE) 
    YAxisStepper.step(600, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    time.sleep (0.1)'''
    
        