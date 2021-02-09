from array import *
from chess_move import ChessMove
'''
Move to one space at a time.
'''
#define pieces
pieces = {
    "bpawn":1,"brook":2,'bknight':3,'bbishop':4,'bqueen':5,'bking':6,
    'wpawn':7,'wrook':8,'wknight':9,'wbishop':10,'wqueen':11,'wking':12
    }

#create reference for board letters and numbers so actual numbers on the board(1-8) work with array(0-7)
reference = {
    'a' : 0 , 'b' : 1 , 'c' : 2 , 'd': 3 , 'e': 4 , 'f': 5 , 'g': 6 , 'h': 7,
    '1': 0 , '2': 1  ,'3': 2  ,'4': 3  ,'5': 4  ,'6' : 5  ,'7': 6  ,'8': 7
    }

current_position = [0,0]
move_position = [0,0]

'''
create board array
letters go left to right starting from a
numbers go down staring from 1
'''
board = [[8,9,10,11,12,10,9,8], \
         [7,7,7,7,7,7,7,7],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [0,0,0,0,0,0,0,0],\
         [1,1,1,1,1,1,1,1],\
         [2,3,4,5,6,4,3,2]]

def take_piece(current, move_position):
    print("take piece", current, board[move_position[1]][move_position[0]])
    if current > 6 and board[move_position[1]][move_position[0]] < 7 and current != 0 and board[move_position[1]][move_position[0]] != 0:
        return True
    elif current < 7 and board[move_position[1]][move_position[0]] > 6 and current != 0 and board[move_position[1]][move_position[0]] != 0:
        return True
    else:
        return False

def print_board():
    for r in board:
            for c in r:
                print(c,end = " ")
            print()

move = ChessMove()

while (True):
    moveTo = input("enter move from and move to   ")  #intake ending position and split into letter and number
    # print(moveTo)
    temp = 0
    knight = False
    
    #try:
    deltaX = reference[moveTo[0]] - current_position[0]
    deltaY = reference[moveTo[1]] - current_position[1]
    print(deltaX, deltaY)

    if deltaX > 0:
        directionX = "positive"
        move_position[0] += deltaX
    else:
        directionX = "negative"
        move_position[0] += deltaX       # negative number

    if deltaY > 0:
        directionY = "positive"
        move_position[1] += deltaY
    else:
        directionY = "negative"
        move_position[1] += deltaY       # negative number

    current_position[0] = move_position[0]
    current_position[1] = move_position[1]
    print(current_position, move_position, abs(deltaX), abs(deltaY), directionX, directionY, "off", board[current_position[1]][current_position[0]])
    move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, "off", False)           




    deltaX2 = reference[moveTo[2]] - current_position[0]
    deltaY2 = reference[moveTo[3]] - current_position[1]
    print(deltaX2, deltaY2)

    if deltaX2 > 0:
        directionX = "positive"
        move_position[0] += deltaX2
    else:
        directionX = "negative"
        move_position[0] += deltaX2       # negative number

    if deltaY2 > 0:
        directionY = "positive"
        move_position[1] += deltaY2
    else:
        directionY = "negative"
        move_position[1] += deltaY2       # negative number

    temp = board[current_position[1]][current_position[0]]
    board[current_position[1]][current_position[0]] = 0
    if temp == 3 or temp == 9:
        knight = True
    else:
        knight = False 


    if take_piece(temp,move_position):
        move.take_piece(abs(deltaX2), abs(deltaY2), directionX, directionY, move_position)
    print(current_position, move_position, abs(deltaX2), abs(deltaY2), directionX, directionY, "on", knight, board[current_position[1]][current_position[0]])
    move.move_steppers_uneven(abs(deltaX2), abs(deltaY2), directionX, directionY, "on", knight)

    current_position[0] = move_position[0]
    current_position[1] = move_position[1]
    board[current_position[1]][current_position[0]] = temp

    print_board()

    #except:
    #    print("invalid entry")
