from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
import random

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()

myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(200, 2)      # 200 steps/rev, motor port #1
myStepper1.setSpeed(60)          # 30 RPM
myStepper2.setSpeed(60)          # 30 RPM

class MotorMove(object):
    def __init(self):
        STEPSTYLE = Adafruit_MotorHAT.DOUBLE
        FORWARD = Adafruit_MotorHAT.FORWARD
        BACKWARD = Adafruit_MotorHAT.BACKWARD

        global st1
        global st2
        global myStepper1
        global myStepper2
    
    def stepper_worker(self, stepper, numsteps, direction, style):
        #print("Steppin!")
        stepper.step(numsteps, direction, style)
        #print("Done")

    def stepper_outandback(self, distance):
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

Chess = MotorMove()
Chess.stepper_outandback(450)
