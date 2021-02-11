from array import *
from chess_move import ChessMove
from time import sleep

'''
assign variables and create objects
'''
move = ChessMove()
current_position = [0,0]
directionX = ""
directionY = ""
turn = 1                    # evens are black moves, odds are white move

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

# garry kasparov v veselin topalov
# https://www.chessgames.com/perl/chessgame?gid=1011478
moveset = ["e2e4", "d7d6", "d2d4", "g8f6", "b1c3", "g7g6", "c1e3", "f8g7", "d1d2", "c7c6", "f2f3", "b7b5", \
            "g1e2", "b8d7", "e3h6", "g7h6", "d2h6", "c8b7", "a2a3", "e7e5", "qc", "d8e7", "c1b1", "a7a6", \
            "e2c1", "qc", "c1b3", "e5d4", "d1d4", "c6c5", "d4d1", "d7b6", "g2g3", "c8b8", "b3a5", "b7a8",\
            "f1h3", "d6d5", "h6f4", "b8a7", "h1e1", "d5d4", "c3d5", "b6d5", "e4d5", "e7d6", "d1d4", "c5d4",\
            "e1e7", "a7b6", "f4d4", "b6a5", "b2b4", "a5a4", "d4c3", "d6d5", "e7a7", "a8b7", "a7b7", "d5c4",\
            "c3f6", "a4a3", "f6a6", "a3b4", "c2c3", "b4c3", "a6a1", "c3d2", "a1b2", "d2d1", "h3f1", "d8d2",\
            "b7d7", "d2d7", "f1c4", "b5c4", "b2h8", "d7d3", "h8a8", "c4c3", "a8a4", "d1e1", "f3f4", "f7f5",\
            "b1c2", "d3d2", "a4a7"]

def take_piece(current, move_position):
    '''
    figure out of moving to a space will take a piece, telling the chess_move program to initiate the algorithm that moves pieces off of the board
    '''
    print("take piece", current, board[move_position[1]][move_position[0]])
    if current > 6 and board[move_position[1]][move_position[0]] < 7 and current != 0 and board[move_position[1]][move_position[0]] != 0:
        return True
    elif current < 7 and board[move_position[1]][move_position[0]] > 6 and current != 0 and board[move_position[1]][move_position[0]] != 0:
        return True
    else:
        return False

def print_board():
    '''
    prints the board out
    '''
    for r in board:
            for c in r:
                print(c,end = " ")
            print()

def find_knight(temp):
    '''
    figure out if a piece is a knight or not, telling the chess_move program to initiate the algorithm that moves pieces on the lines
    '''
    if temp == 3 or temp == 9:
        return True
    else:
        return False

def calculate_moves(x, y):
    '''
    calculate the number of steps needed to move to a certain square
    '''
    global directionX
    global directionY
    global current_position
    
    if x > 0:
        directionX = "positive"
        current_position[0] += x
    else:
        directionX = "negative"
        current_position[0] += x       # negative number

    if y > 0:
        directionY = "positive"
        current_position[1] += y
    else:
        directionY = "negative"
        current_position[1] += y       # negative number

def piece_color(piece):
    '''
    determine color of a piece, white will return True
    '''
    if piece > 6:
        return True
    else:
        return False

def find_turn(numTurn):
    '''
    determine whose turn it is, white will return True
    '''
    if numTurn%2 == 1:
        return True
    else:
        return False

print("e2e4: move pawn to e4 \nkc:kingside castle \nqc:queenside castle \nhome:return to a1")

while (True):
    #moveTo = input("INPUT: ")  #intake ending position and split into letter and number
    moveTo = moveset[turn - 1]
    print(moveTo, (turn-1))
    # print(moveTo)
    TEMP = 0
    KNIGHT = False

    if moveTo == "qc" and find_turn(turn):
        deltaX = 4 - current_position[0]
        deltaY = 0 - current_position[1]
        calculate_moves(deltaX, deltaY)

        board[0][4] = 0
        board[0][2] = 12
        board[0][0] = 0
        board[0][3] = 8
        move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, "off", False)
        move.queenside_castle()

    elif moveTo == "kc" and find_turn(turn):
        deltaX = 4 - current_position[0]
        deltaY = 0 - current_position[1]
        calculate_moves(deltaX, deltaY)

        board[0][4] = 0
        board[0][6] = 12
        board[0][7] = 0
        board[0][5] = 8
        move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, "off", False)
        move.kingside_castle()

    elif moveTo == "qc" and not find_turn(turn):
        deltaX = 4 - current_position[0]
        deltaY = 7 - current_position[1]
        calculate_moves(deltaX, deltaY)

        board[7][4] = 0
        board[7][2] = 6
        board[7][0] = 0
        board[7][3] = 2
        move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, "off", False)
        move.queenside_castle()

        move.move_steps_uneven(0,60,"positive", "positive")     # temporary workaround to topping out

    elif moveTo == "kc" and not find_turn(turn):
        deltaX = 4 - current_position[0]
        deltaY = 7 - current_position[1]
        calculate_moves(deltaX, deltaY)

        board[7][4] = 0
        board[7][6] = 6
        board[7][7] = 0
        board[7][5] = 2
        move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, "off", False)
        move.kingside_castle()

        move.move_steps_uneven(0,60,"positive", "positive")     # temporary workaround to topping out

    elif moveTo == "home":
        move.return_origin()

    else:
        #try:
        deltaX = reference[moveTo[0]] - current_position[0]
        deltaY = reference[moveTo[1]] - current_position[1]
        print(deltaX, deltaY)
        calculate_moves(deltaX, deltaY)

        TEMP = board[current_position[1]][current_position[0]]
        board[current_position[1]][current_position[0]] = 0
        KNIGHT = find_knight(TEMP)


        #print(current_position, move_position, abs(deltaX), abs(deltaY), directionX, directionY, "off", board[current_position[1]][current_position[0]])
        move.move_steppers_uneven(abs(deltaX), abs(deltaY), directionX, directionY, "off", False)           

        deltaX2 = reference[moveTo[2]] - current_position[0]
        deltaY2 = reference[moveTo[3]] - current_position[1]
        print(deltaX2, deltaY2)
        calculate_moves(deltaX2, deltaY2)

        
        if take_piece(TEMP,current_position):
            move.take_piece(abs(deltaX2), abs(deltaY2), directionX, directionY, current_position)
        #print(current_position, move_position, abs(deltaX2), abs(deltaY2), directionX, directionY, "on", KNIGHT, board[current_position[1]][current_position[0]])
        move.move_steppers_uneven(abs(deltaX2), abs(deltaY2), directionX, directionY, "on", KNIGHT)

        board[current_position[1]][current_position[0]] = TEMP      # moving pieces in virtual chessboard
    turn += 1                                                   # keeping track of whose turn it is
    print_board()

        #except:
        #    print("invalid entry")
