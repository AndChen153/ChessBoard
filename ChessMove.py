

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import RPi.GPIO as GPIO
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
st3 = threading.Thread()

# setup gpio pin for relay
channel = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


# turns off motors at exit of program
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
def killThreads():
    st1.kill()
    st1.join()

atexit.register(turnOffMotors)

# magnet relay control
stop_threads=False
def magnetOnOff(magnet):
    global stop_threads
    while True:
        if magnet == "1":
            GPIO.output(channel, GPIO.HIGH)
        elif magnet == "0":
            GPIO.output(channel, GPIO.LOW)
        print("running magnet_____________")
        if stop_threads:
            break

# runs motors
def stepper_worker(stepper, numsteps, direction, style):
    print("Steppin!")
    #magnetOnOff(magnet)
    stepper.step(numsteps, direction, style)
    print("Done \n")

XAxisStepper = mh.getStepper(200, 1)      # 200 steps/rev (1.8 degrees per step), motor port #1
YAxisStepper = mh.getStepper(200, 2)      # 200 steps/rev (1.8 degrees per step), motor port #2
XAxisStepper.setSpeed(60)
YAxisStepper.setSpeed(60)

# use double or interleave(half the distnace double moves)
stepStyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3
stepDirection = [Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.BACKWARD]
#                   0                               1
stepDirectiony = [Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.FORWARD]
# so motors move same direction    0                               1


# number of steps per spaces on the chessboard
steps=230
ysteps=230
incrementer=0

time.sleep(5)
print('setup complete')


def jiggleX(xTemp):
    global st1
    global st2
    if not st2.is_alive():
        st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
        st2.start()
    if xTemp > 300:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if xTemp > 600:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if xTemp > 900:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if xTemp > 1200:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if xTemp > 1500:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()

def jiggleY(yTemp):
    global st1
    global st2
    if not st1.is_alive():
        st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 3, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
        st1.start()
    if yTemp > 300:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if yTemp > 600:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if yTemp > 900:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if yTemp > 1200:
        time.sleep(4)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if yTemp > 1500:
        time.sleep(43)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 3, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()

# direction -> 0 is forward 1 is backward
def translation(xPlaces, xDirection, yPlaces, yDirection, magnet):
    global st1
    global st2
    xPlaces = int(xPlaces)*steps
    yPlaces = int(yPlaces)*ysteps
    print(yPlaces)
    dirx = stepDirection[int(xDirection)]
    diry = stepDirectiony[int(yDirection)]
    
    st3 = threading.Thread(target=magnetOnOff, args=(magnet))
    st3.start()

    # moving in a diagonal
    if xPlaces == yPlaces:
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xPlaces, dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yPlaces, diry, stepStyles[1],))
            st2.start()



    # un-diagonal movement
    elif xPlaces > yPlaces:

        xTemp = xPlaces - yPlaces
        
        # diagonal
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(yPlaces), dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, int(yPlaces), diry, stepStyles[1],))
            st2.start()

        # straight
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move x ")
            time.sleep(0.5)
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xTemp, dirx, stepStyles[1],))
            st1.start()
            
            
        # uses other motor for a small amount to get rid of st1 not completing full amount of steps bc of weird motor hat
        jiggleX(xTemp)

    elif yPlaces > xPlaces:

        yTemp = yPlaces-xPlaces

        # diagonal
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(xPlaces), dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper,int(xPlaces), diry, stepStyles[1],))
            st2.start()

        # straight
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move y ")
            time.sleep(0.5)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yTemp, diry, stepStyles[1],))
            st2.start()
        # uses other motor for a small amount to get rid of st2 not completing full amount of steps bc of weird motor hat
        jiggleY(yTemp)
    
    
    turnOffMotors()

# sys.argv=(xPlaces, xDirection, yPlaces, yDirection)
#            0          1           2          3

magnet=input("1(high) or 0(low)")
a=input("places")
b=input("direction")
c=input("places")
d=input("direction")
translation(a, b, c, d, magnet)



GPIO.cleanup()
stop_threads = True


'''
if not st1.is_alive():
    st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(x), dirx, stepStyles[2],))
    st1.start()
if not st2.is_alive():
    st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, int(y), diry, stepStyles[2],))
    st2.start()
'''