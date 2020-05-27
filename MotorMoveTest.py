#to find the number of steps for each square on the chessboard

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

import time
import atexit
import threading

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()

XAxisStepper = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
#YAxisStepper = mh.getStepper(200, 2)      # 200 steps/rev, motor port #1
XAxisStepper.setSpeed(50)
#YAxisStepper.setSpeed(20)


# turns off motors at exit of program
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)


stepStyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3

stepDirection = [Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.BACKWARD]
#                   0                               1

def stepper_worker(stepper, numsteps, direction, style):
    print("Steppin!")
    stepper.step(numsteps, stepDirection[int(direction)], stepStyles[int(style)])
    print("Done \n")



while (True):
    x=input("x axis? \n")
    direction = input("direction? \n")

    stepper_worker(XAxisStepper, int(x), int(direction), 2)

    turnOffMotors()



    '''
    YAxisStepper.step(600, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    XAxisStepper.step(600, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    time.sleep (0.1)
    XAxisStepper.step(600, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE) 
    YAxisStepper.step(600, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    time.sleep (0.1)'''
    
        