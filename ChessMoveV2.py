from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
import random

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

class MotorMove(object):
    def __init(self):
        self.STEPSTYLE = Adafruit_MotorHAT.DOUBLE
        self.FORWARD = Adafruit_MotorHAT.FORWARD
        self.BACKWARD = Adafruit_MotorHAT.BACKWARD

        # create a default object, no changes to I2C address or frequency
        self.mh = Adafruit_MotorHAT()

        # create empty threads (these will hold the stepper 1 and 2 threads)
        self.st1 = threading.Thread()
        self.st2 = threading.Thread()

        self.myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
        self.myStepper2 = mh.getStepper(200, 2)      # 200 steps/rev, motor port #1
        self.myStepper1.setSpeed(60)          # 30 RPM
        self.myStepper2.setSpeed(60)          # 30 RPM
    
    def stepper_worker(self, stepper, numsteps, direction, style):
        #print("Steppin!")
        stepper.step(numsteps, direction, style)
        #print("Done")

    def stepper_outandback(self, distance):
        if not self.st1.isAlive():
            self.st1 = threading.Thread(target=stepper_worker, args=(self.myStepper1, distance, self.FORWARD, self.STEPSTYLE,))
            self.st1.start()

        if not self.st2.isAlive():
            self.st2 = threading.Thread(target=stepper_worker, args=(self.myStepper2, distance, self.FORWARD, self.STEPSTYLE,))
            self.st2.start()

        self.st1.join()
        self.st2.join()

        if not self.st1.isAlive():
            self.st1 = threading.Thread(target=stepper_worker, args=(self.myStepper1, distance, self.BACKWARD, self.STEPSTYLE,))
            self.st1.start()

        if not self.st2.isAlive():
            self.st2 = threading.Thread(target=stepper_worker, args=(self.myStepper2, distance, self.BACKWARD, self.STEPSTYLE,))
            self.st2.start()

Chess = MotorMove()
Chess.stepper_outandback(450)
