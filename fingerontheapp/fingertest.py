from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit
import time
import atexit
import threading
import random
import sys

# create a default object, no changes to I2C address or frequency
kit = MotorKit()

# create empty threads (these will hold the stepper 1 and 2 threads) so both motors can be ran at the same time
st1 = threading.Thread()
st2 = threading.Thread()

def turnOffMotors():
    kit.stepper1.release()
    kit.stepper2.release()


def killThreads():
    st1.kill()
    st1.join()
    st2.kill()
    st2.join()

atexit.register(turnOffMotors)


# runs motors
def stepper_worker(stepper, numsteps, direction, style):
    # print("Steppin!")
    for _ in range(numsteps):
        stepper.onestep(direction=direction, style=style)
    # print("Done")


# use double or interleave(will take 400 steps per 1 rev)     DO NOT use single or microstep, these lead to very poor motor movement
stepStyles = [STEPPER.SINGLE, STEPPER.DOUBLE, STEPPER.INTERLEAVE, STEPPER.MICROSTEP]
#                   0                               1                           2                           3
stepDirection = [STEPPER.FORWARD, STEPPER.BACKWARD]
#                   0                               1
stepDirectiony = [STEPPER.BACKWARD, STEPPER.FORWARD]
# so motors move same direction    0                               1


# number of steps per spaces on the chessboard
steps=220
ysteps=220
incrementer=0

print('setup complete')



# direction -> 0 is negative direction 1 is positive direction
def translation(xPlaces, xDirection, yPlaces, yDirection):
    global st1
    global st2
    xPlaces = int(xPlaces)*steps
    yPlaces = int(yPlaces)*ysteps
    dirx = stepDirection[int(xDirection)]
    diry = stepDirectiony[int(yDirection)]

    # moving in a diagonal 
    if xPlaces == yPlaces:
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, xPlaces, dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, yPlaces, diry, stepStyles[1],))
            st2.start()

    # un-diagonal movement
    elif xPlaces > yPlaces:

        xTemp = xPlaces - yPlaces
        
        # diagonal movement
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, int(yPlaces), dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, int(yPlaces), diry, stepStyles[1],))
            st2.start()

        # straight movement
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move x ")
            time.sleep(0.5)
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, xTemp, dirx, stepStyles[1],))
            st1.start()
            

    elif yPlaces > xPlaces:

        yTemp = yPlaces-xPlaces

        # diagonal movement
        if not st1.is_alive():
            st1 = threading.Thread(target=stepper_worker, args=(kit.stepper1, int(xPlaces), dirx, stepStyles[1],))
            st1.start()
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2,int(xPlaces), diry, stepStyles[1],))
            st2.start()

        # straight movement
        while st1.is_alive() and st2.is_alive():
            print("waiting.. move y ")
            time.sleep(0.5)
        if not st2.is_alive():
            st2 = threading.Thread(target=stepper_worker, args=(kit.stepper2, yTemp, diry, stepStyles[1],))
            st2.start()
    
    
    turnOffMotors()


a=input("places")
b=input("direction")
c=input("places")
d=input("direction")

translation(a, b, c, d)

