from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
kit = MotorKit()

#stepper 1 controls the x axis and stepper 2 controls the y axis
#0,0 is bottom left corner of board on white side


totalXSteps = 0
totalYSteps = 0

def moveSteps(x,y):
    for i in range(x):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    for i in range(y):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)

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

    
moveSteps(500,500)
kit.stepper1.release()
kit.stepper2.release()