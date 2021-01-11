from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
import random

STEPSTYLE = Adafruit_MotorHAT.DOUBLE
FORWARD = Adafruit_MotorHAT.FORWARD
BACKWARD = Adafruit_MotorHAT.BACKWARD

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()

def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(200, 2)      # 200 steps/rev, motor port #1
myStepper1.setSpeed(60)          # 30 RPM
myStepper2.setSpeed(60)          # 30 RPM

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

while (True):
    if not st1.isAlive():
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 200, FORWARD, STEPSTYLE,))
        st1.start()

    if not st2.isAlive():
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 200, FORWARD, STEPSTYLE,))
        st2.start()
    
    time.sleep(5)
    st1.join()
    st2.join()

    if not st1.isAlive():
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 200, BACKWARD, STEPSTYLE,))
        st1.start()

    if not st2.isAlive():
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 200, BACKWARD, STEPSTYLE,))
        st2.start()
    
    time.sleep(5)
    st1.join()
    st2.join()