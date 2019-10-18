import time
import atexit
import threading
import random
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

# create a default object, no changes to I2C address or frequency
kit = MotorKit()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()

atexit.register(turnOffMotors)

S1 = mh.getStepper(200, 1)     # 200 steps/rev, motor port #1
S2 = mh.getStepper(200, 2)     # 200 steps/rev, motor port #1

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

def stepper_worker(stepper, numsteps, direction, style):
   print("Steppin!")
   stepper.step(numsteps, direction, style)
   print("Done")

while (True):
    if not st1.isAlive():

      randomdir = 0#random.randint(0, 1)
      print("Stepper 1"),
      if (randomdir == 0):
         dir = Adafruit_MotorHAT.FORWARD
         print("forward"),
      else:
         dir = Adafruit_MotorHAT.BACKWARD
         print("backward"),
      randomsteps = 200

      print("%d steps" % randomsteps)
      #st1 = threading.Thread(target=stepper_worker, args=(S1, randomsteps, dir, stepstyles[1],))
      st1 = threading.Thread(target=stepper_worker, args=(S1, 200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE,))
      st1.start()

    if not st2.isAlive():
      print("Stepper 2"),
      randomdir = 0#random.randint(0, 1)
      if (randomdir == 0):
         dir = Adafruit_MotorHAT.FORWARD
         print("forward"),
      else:
         dir = Adafruit_MotorHAT.BACKWARD
         print("backward"),

      randomsteps = 200      
      print("%d steps" % randomsteps)

      st2 = threading.Thread(target=stepper_worker, args=(S2, randomsteps, dir, stepstyles[1],))
      st2.start()
    time.sleep(0.1)

kit.stepper1.release()
kit.stepper2.release()















#stepper 1 controls the x axis and stepper 2 controls the y axis
#0,0 is bottom left corner of board on white side

'''
totalXSteps = 0
totalYSteps = 0

def moveSteps(x,y):
    for i in range(x):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    for i in range(y):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)

def moveTo(x, y , currentX , currentY):
    if (x < currentX):
        steps = 100*(x-currentX)

        totalXSteps+=steps
        for i in range(steps):
            kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)

    elif (x > currentX):
        steps = 100*(currentX-x)
        totalXSteps-=steps
        for i in range(steps):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)

    if (y < currentY):
        steps = 100*(y-currentY)
        totalYSteps+=steps
        for i in range(steps):
            kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)

    elif (y > currentY):
        steps = 100*(currentY-y)
        totalYSteps-=steps
        for i in range(steps):
            kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)






#move back to 0,0
def zero():
    for i in range(totalXSteps):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)

    for i in range(totalYSteps):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)






#move to position first using moveTo then use takePiece to move piece off board
#true is white false is black
def takePiece(pieceColor):
    #move peice to grid line back and to the left to take it off the board without disturbing other peices
    for i in range(50):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)

    totalXSteps -= 50
    totalYSteps -= 50

    if (pieceColor):
        for i in range(totalYSteps):
            kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
    
    else:
        for i in range(8000-totalYSteps):
            kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
'''
