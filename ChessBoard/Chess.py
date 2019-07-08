#import from adafruit_motor import stepper
from array import *
#from adafruit_motorkit import MotorKit
#from StepperMove import moveSteps, moveTo, zero, takePiece

pieces = {"bpawn":1,"brook":2,'bknight':3,'bbishop':4,'bqueen':5,'bking':6,     'wpawn':7,'wrook':8,'wknight':9,'wbishop':10,'wqueen':11,'wking':12}
reference = {'a' : 0 , 'b' : 1 , 'c' : 2 , 'd': 3 , 'e': 4 , 'f': 5 , 'g': 6 , 'h': 7 , '1': 0 , '2': 1  ,'3': 2  ,'4': 3  ,'5': 4  ,'6' : 5  ,'7': 6  ,'8': 7}


#letters go left to right starting from a
#numbers go down staring from 1
board = [[2,3,4,5,6,4,3,2], \
         [1,1,1,1,1,1,1,1],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [7,7,7,7,7,7,7,7],\
         [8,9,10,11,12,10,9,8]]




while (True):
    startingPos=input("enter starting position spaces inbetween")
    endingPos=input("enter ending position spaces inbetween")

    startingPosList = startingPos.split()
    endingPosList = endingPos.split()

    startletter = startingPosList[0]
    startnumber = startingPosList[1]

    endletter = endingPosList[0]
    endnumber = endingPosList[1]

    temp = board[reference[startnumber]][reference[startletter]]

    board[reference[startnumber]][reference[startletter]] = 0
    board[reference[endnumber]][reference[endletter]] = temp

    print (board[reference[startnumber]][reference[startletter]])
    print (board[reference[endnumber]][reference[endletter]])


    

    
