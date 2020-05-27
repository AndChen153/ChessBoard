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

myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(200, 2)      # 200 steps/rev, motor port #1
myStepper1.setSpeed(60)          # 30 RPM
myStepper2.setSpeed(60)          # 30 RPM

stepStyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3

stepDirection = [Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.BACKWARD]
#                   0                               1

def stepper_worker(stepper, numsteps, direction, style):
    print("Steppin!"+ str(numsteps) + stepDirection[direction] + stepStyles[style])
    stepper.step(numsteps, stepDirection[int(direction)], stepStyles[int(style)])
    print("Done")

'''myStepper1.step(30, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
time.sleep (0.1)
myStepper1.step(30, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
time.sleep (0.1)
print("set")'''


while (True):
    x=input("x axis?")
    direction = input("direction?")

    stepper_worker(myStepper1, int(x), int(direction), 2)

    turnOffMotors()



    '''
    myStepper2.step(600, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    myStepper1.step(600, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    time.sleep (0.1)
    myStepper1.step(600, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE) 
    myStepper2.step(600, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    time.sleep (0.1)'''
    
        



# turns off motors at exit of program
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)