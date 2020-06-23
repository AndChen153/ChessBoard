from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import RPi.GPIO as GPIO
import time
import atexit
import threading
import random
import sys

# do not cleanup gpio, will cause the relay to switch off as soon as the motors start to move

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads) so both motors can be ran at the same time
st1 = threading.Thread()
st2 = threading.Thread()

# setup gpio pin for triggering relay
channel = 17
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
    st2.kill()
    st2.join()

atexit.register(turnOffMotors)

# magnet relay control
stop_threads=False
def magnetOnOff(magnet):
    if magnet == "1":
        GPIO.output(channel, GPIO.HIGH)
    elif magnet == "0":
        GPIO.output(channel, GPIO.LOW)
    
    '''
    global stop_threads
    while True:
        if magnet == "1":
            GPIO.output(channel, GPIO.HIGH)
        elif magnet == "0":
            GPIO.output(channel, GPIO.LOW)
        time.sleep(0.2)
        print("running magnet_____________")
        if stop_threads:
            break
    '''

# runs motors
def stepper_worker(stepper, numsteps, direction, style):
    print("Steppin!")
    #magnetOnOff(magnet)
    stepper.step(numsteps, direction, style)
    print("Done \n")

# setting up stepper motors
XAxisStepper = mh.getStepper(200, 1)      # 200 steps/rev (1.8 degrees per step), motor port #1
YAxisStepper = mh.getStepper(200, 2)      # 200 steps/rev (1.8 degrees per step), motor port #2
# not sure if this will affect anything
XAxisStepper.setSpeed(5000)
YAxisStepper.setSpeed(5000)

# use double or interleave(will take 400 steps per 1 rev)     DO NOT use single or microstep, these lead to very poor motor movement
stepStyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]
#                   0                               1                           2                           3
stepDirection = [Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.BACKWARD]
#                   0                               1
stepDirectiony = [Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.FORWARD]
# so motors move same direction    0                               1


# number of steps per spaces on the chessboard
steps=220
ysteps=220
incrementer=0

print('setup complete')


def jiggleX(xTemp):
    global st1
    global st2
    time.sleep(1)
    if not st2.is_alive():
        st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
        st2.start()
    if xTemp > 300:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if xTemp > 600:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if xTemp > 900:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if xTemp > 1200:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if xTemp > 1500:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()

def jiggleY(yTemp):
    global st1
    global st2
    time.sleep(1)
    if not st1.is_alive():
        st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, 1, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
        st1.start()
    if yTemp > 300:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if yTemp > 600:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if yTemp > 900:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()
    if yTemp > 1200:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.FORWARD, stepStyles[1],))
            st2.start()
    if yTemp > 1500:
        time.sleep(4.65)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, 1, Adafruit_MotorHAT.BACKWARD, stepStyles[1],))
            st2.start()

# direction -> 0 is negative direction 1 is positive direction
def translation(xPlaces, xDirection, yPlaces, yDirection, magnet):
    global st1
    global st2
    xPlaces = int(xPlaces)*steps
    yPlaces = int(yPlaces)*ysteps
    dirx = stepDirection[int(xDirection)]
    diry = stepDirectiony[int(yDirection)]

    magnetOnOff(magnet)

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
        
        # diagonal movement
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(yPlaces), dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, int(yPlaces), diry, stepStyles[1],))
            st2.start()

        # straight movement
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move x ")
            time.sleep(0.5)
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, xTemp, dirx, stepStyles[1],))
            st1.start()
            
        # uses other motor for a small amount to get rid of st1 not completing full amount of steps bc of weird motor hat behavior
        jiggleX(xTemp)

    elif yPlaces > xPlaces:

        yTemp = yPlaces-xPlaces

        # diagonal movement
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(xPlaces), dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper,int(xPlaces), diry, stepStyles[1],))
            st2.start()

        # straight movement
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move y ")
            time.sleep(0.5)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, yTemp, diry, stepStyles[1],))
            st2.start()
        # uses other motor for a small amount to get rid of st2 not completing full amount of steps bc of weird motor hat behavior
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





'''
if not st1.is_alive():
    st1 = threading.Thread(target=stepper_worker, args=(XAxisStepper, int(x), dirx, stepStyles[2],))
    st1.start()
if not st2.is_alive():
    st2 = threading.Thread(target=stepper_worker, args=(YAxisStepper, int(y), diry, stepStyles[2],))
    st2.start()
'''