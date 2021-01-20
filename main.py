from array import *
from chess_move import ChessMove


#define pieces
pieces = {"bpawn":1,"brook":2,'bknight':3,'bbishop':4,'bqueen':5,'bking':6,     'wpawn':7,'wrook':8,'wknight':9,'wbishop':10,'wqueen':11,'wking':12}

#create reference for board letters and numbers so actual numbers on the board(1-8) work with array(0-7)
reference = {'a' : 0 , 'b' : 1 , 'c' : 2 , 'd': 3 , 'e': 4 , 'f': 5 , 'g': 6 , 'h': 7 , '1': 0 , '2': 1  ,'3': 2  ,'4': 3  ,'5': 4  ,'6' : 5  ,'7': 6  ,'8': 7}

current_position = [0,0]

'''
create board array
letters go left to right starting from a
numbers go down staring from 1
'''
board = [[2,3,4,5,6,4,3,2], \
         [1,1,1,1,1,1,1,1],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [7,7,7,7,7,7,7,7],\
         [8,9,10,11,12,10,9,8]]

move = ChessMove()

while (True):
    moveTo = input("enter ending position (lower case letters) and o or f for electromagnet")  #intake ending position and split into letter and number
    print(moveTo)
    try:
        deltaX = reference[moveTo[0]] - current_position[0]
        deltaY = reference[moveTo[1]] - current_position[1]

        if deltaX > 0:
            directionX = "positive"
            current_position[0] += deltaX
        else:
            directionX = "negative"
            current_position[0] += deltaX       # negative number

        if deltaY > 0:
            directionY = "positive"
            current_position[1] += deltaY
        else:
            directionY = "negative"
            current_position[1] += deltaY       # negative number

        if moveTo[2] == "o":
            magnet = "on"
        else:
            magnet = "off"

        print(current_position, abs(deltaX), abs(deltaY), directionX, directionY, magnet)
        move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, magnet)
    except:
        print("please enter valid integer")

