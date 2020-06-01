

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
import random
import sys

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads) so both motors can be ran at the same time
st1 = threading.Thread()
st2 = threading.Thread()

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

XAxisStepper = mh.getStepper(200, 1)      # 200 steps/rev (1.8 degrees per step), motor port #1
YAxisStepper = mh.getStepper(200, 2)      # 200 steps/rev (1.8 degrees per step), motor port #2
XAxisStepper.setSpeed(5000)
YAxisStepper.setSpeed(5000)

#use double or interleave(half the distnace double moves)
stepStyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3
stepDirection = [Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.BACKWARD]
#                   0                               1


#number of steps per spaces on the chessboard
steps=200

time.sleep(5)
print('setup complete')

#to prevent weird motor movements (stops moving halfway) while only moving one motor
def jiggle():
    global st1
    global st2
    print('jiggle')
    run = 0
    while st1.is_alive():
        if not st2.is_alive() and run == 0:
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 5, stepDirection[0], stepStyles[0],))
            st2.start()
            run = 1
            print("jigglef1")

        if not st2.is_alive() and run == 1:
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 5, stepDirection[1], stepStyles[0],))
            st2.start()
            run = 0
            print("jiggleb1")
            

    while st2.is_alive():
        if not st1.is_alive() and run == 0:
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 5, stepDirection[0], stepStyles[0],))
            st1.start()
            run = 1
            print("jigglef2")

        if not st1.is_alive() and run == 1:
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 5, stepDirection[1], stepStyles[0],))
            st1.start()
            run = 0
            print("jiggleb2")




#direction -> 0 is forward 1 is backward
def translation(xPlaces, xDirection, yPlaces, yDirection):
    global st1
    global st2
    run = 0
    xPlaces = int(xPlaces)*steps
    yPlaces = int(yPlaces)*steps
    dirx = stepDirection[int(xDirection)]
    diry = stepDirection[int(yDirection)]


    #moving in a diagonal
    if xPlaces == yPlaces:
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xPlaces, dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yPlaces, diry, stepStyles[1],))
            st2.start()



    #un-diagonal movement
    elif xPlaces > yPlaces:

        xTemp = xPlaces - yPlaces

        #diagonal
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, yPlaces, dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yPlaces, diry, stepStyles[1],))
            st2.start()

        #straight
        while st1.is_alive() and st2.is_alive():
            print("waiting..")
            time.sleep(0.5)
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xTemp, dirx, stepStyles[1],))
            st1.start()
            '''while True:
                if not st2.is_alive() and run == 0:
                    st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 5, stepDirection[0], stepStyles[0],))
                    st2.start()
                    run = 1
                    print("jigglef1")

                if not st2.is_alive() and run == 1:
                    st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 5, stepDirection[1], stepStyles[0],))
                    st2.start()
                    run = 0
                    print("jiggleb1")
                if not st1.is_alive():
                    break'''
    

    elif yPlaces > xPlaces:

        yTemp = yPlaces-xPlaces

        #diagonal
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xPlaces, dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper,xPlaces, diry, stepStyles[1],))
            st2.start()

        #straight
        while st1.is_alive() and st2.is_alive():
            print("waiting..")
            time.sleep(0.5)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yTemp, diry, stepStyles[1],))
            st2.start()
            '''while True:
                if not st1.is_alive() and run == 0:
                    st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 5, stepDirection[0], stepStyles[0],))
                    st1.start()
                    run = 1
                    print("jigglef2")

                if not st1.is_alive() and run == 1:
                    st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 5, stepDirection[1], stepStyles[0],))
                    st1.start()
                    run = 0
                    print("jiggleb2")
                if not st2.is_alive():
                    break'''

    turnOffMotors()

#sys.argv=(xPlaces, xDirection, yPlaces, yDirection)
#            0          1           2          3
if len(sys.argv)>3:
    translation(sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3])


translation(3,1,0,1)
time.sleep(0.1)




'''
if not st1.is_alive():
    st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(x), dirx, stepStyles[2],))
    st1.start()
if not st2.is_alive():
    st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, int(y), diry, stepStyles[2],))
    st2.start()
'''