from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import threading


# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3

def stepper_worker(stepper, numsteps, direction, style):
    print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(200, 2)      # 200 steps/rev, motor port #1
myStepper1.setSpeed(45)          # 30 RPM
myStepper2.setSpeed(45)          # 30 RPM
'''
st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 300, Adafruit_MotorHAT.FORWARD, stepstyles[2]))
st1.start()
st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 300, Adafruit_MotorHAT.FORWARD, stepstyles[2]))
st2.start()'''

'''
direction1=True
direction2=True
while (True):
    if not st1.isAlive():
        if direction1:
            dir=Adafruit_MotorHAT.FORWARD
            direction1=False
        else:
            dir=Adafruit_MotorHAT.BACKWARD
            direction1=True
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 300, dir, stepstyles[2]))
        st1.start()

    if not st2.isAlive():
        if direction2:
            dir=Adafruit_MotorHAT.FORWARD
            direction2=False
        else:
            dir=Adafruit_MotorHAT.BACKWARD
            direction2=True
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 300, dir, stepstyles[2]))
        st2.start()'''

while (True):
    myStepper1.step(300, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    myStepper2.step(300, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    myStepper1.step(300, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    myStepper2.step(300, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
        