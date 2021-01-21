from array import *
from chess_move import ChessMove


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

def take_piece(current_position, move_position):
    if board[current_position[1]][current_position[0]] > 6 and board[move_position[1]][move_position[0]] < 7:
        return True
    elif board[current_position[1]][current_position[0]] < 7 and board[move_position[1]][move_position[0]] > 6:
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
    moveTo = input("enter ending position (lower case letters) and o or f for electromagnet  ")  #intake ending position and split into letter and number
    # print(moveTo)
    temp = 0
    
    try:
        print(reference[moveTo[0]], current_position[0])
        print(reference[moveTo[1]], current_position[1])
        deltaX = reference[moveTo[0]] - current_position[0]
        deltaY = reference[moveTo[1]] - current_position[1]
        
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
        
        if moveTo[2] == "o":
            magnet = "on"
            temp = board[current_position[1]][current_position[0]]
            board[current_position[1]][current_position[0]] = 0
            board[move_position[1]][move_position[0]]=temp

            if temp == 3 or temp == 9:
                knight = True
            else:
                knight = False
        else:
            magnet = "off"
        

        '''if take_piece(current_position,move_position) and magnet == "on":
            print("take piece")
            move.power_on()
            move.take_piece(abs(deltaX), abs(deltaY), directionX, directionY, move_position)'''
        
        print(current_position, move_position, abs(deltaX), abs(deltaY), directionX, directionY, magnet, knight, board[current_position[1]][current_position[0]])

        
        move.power_on()
        move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, magnet, knight)

        
        current_position = move_position

        print_board()


    except:
        print("please enter valid integer")

