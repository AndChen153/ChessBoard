from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
kit = MotorKit()

def stopMotors():
    kit.stepper1.release()
    kit.stepper2.release()


def doubleStepOneRotation(motorNum):
    if motorNum==1:
        for i in range(200):
            kit.stepper1.onestep(direction=stepper.FORWARD , style=stepper.DOUBLE)
    if motorNum==2:
        for i in range(200):
            kit.stepper2.onestep(direction=stepper.FORWARD , style=stepper.DOUBLE)

def doubleStepOneRotationB(motorNum):
    if motorNum==1:
        for i in range(200):
            kit.stepper1.onestep(direction=stepper.BACKWARD , style=stepper.DOUBLE)
    if motorNum==2:
        for i in range(200):
            kit.stepper2.onestep(direction=stepper.BACKWARD , style=stepper.DOUBLE)

def interleaveOneRotation(motorNum):
    if motorNum==1:
        for i in range(400):
            kit.stepper1.onestep(direction=stepper.FORWARD , style=stepper.INTERLEAVE)
    if motorNum==2:
        for i in range(400):
            kit.stepper2.onestep(direction=stepper.FORWARD , style=stepper.INTERLEAVE)

def interleaveOneRotationB(motorNum):
    if motorNum==1:
        for i in range(400):
            kit.stepper1.onestep(direction=stepper.BACKWARD , style=stepper.INTERLEAVE)
    if motorNum==2:
        for i in range(400):
            kit.stepper2.onestep(direction=stepper.BACKWARD , style=stepper.INTERLEAVE)

def microstepOneRotation(motorNum):
    if motorNum==1:
        for i in range(3200):
            kit.stepper1.onestep(direction=stepper.FORWARD , style=stepper.MICROSTEP)
    if motorNum==2:
        for i in range(3200):
            kit.stepper2.onestep(direction=stepper.FORWARD , style=stepper.MICROSTEP)

for i in range(3):
    doubleStepOneRotation(2)

    doubleStepOneRotation(2)
    doubleStepOneRotation(2)
    doubleStepOneRotationB(2)

    doubleStepOneRotationB(2)
    doubleStepOneRotationB(2)


stopMotors()
