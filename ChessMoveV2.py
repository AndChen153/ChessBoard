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
def stepper_outandback(distance):
    global st1
    global st2
    if not st1.isAlive():
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, distance, FORWARD, STEPSTYLE,))
        st1.start()

    if not st2.isAlive():
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, distance, FORWARD, STEPSTYLE,))
        st2.start()

    st1.join()
    st2.join()

    if not st1.isAlive():
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, distance, BACKWARD, STEPSTYLE,))
        st1.start()

    if not st2.isAlive():
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, distance, BACKWARD, STEPSTYLE,))
        st2.start()
    
def stepper_outandside(xdistance, ydistance, direction):
    global st1
    global st2
    if xdistance < ydistance:
        distance = xdistance
        remain = ydistance - xdistance
        xfirst = True
    else:
        distance = ydistance
        remain = xdistance - ydistance
        xfirst = False
    
    if not st1.isAlive():
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, distance, direction, STEPSTYLE,))
        st1.start()

    if not st2.isAlive():
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, distance, direction, STEPSTYLE,))
        st2.start()

    st1.join()
    st2.join()

    if xfirst and not st1.isAlive():
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, remain, direction, STEPSTYLE,))
        st1.start()

    if not xfirst and not st2.isAlive():
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, remain, direction, STEPSTYLE,))
        st2.start()

stepper_outandside(0, 1000, FORWARD)
time.sleep(30)
stepper_outandside(0, 1000, BACKWARD)
