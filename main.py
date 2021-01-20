from array import *
#from chess_move import ChessMove


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

#move = ChessMove()

print("start")

while (True):
    moveTo = input("enter ending position (lower case letters)")  #intake ending position and split into letter and number
    print(moveTo)

    deltaX = reference[moveTo[0]] - current_position[0]
    deltaY = reference[moveTo[1]] - current_position[1]

    if deltaX > 0:
        directionX = "positive"
    else:
        directionX = "negative"

    if deltaY > 0:
        directionY = "positive"
    else:
        direcitonY = "negative"

    print(deltaX, deltaY, directionX, direcitonY)


