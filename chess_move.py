'''
program to move the stepper motors depending on how many spaces are inputted
'''

from time import sleep
import RPi.GPIO as GPIO

# 7000 steps per block

class ChessMove:
    def __init__(self):
        self.DIR1 = 21                              # Directional GPIO Pin
        self.STEP1 = 20                             # Step GPIO Pin
        self.DIR2 = 16                              # Directional GPIO Pin
        self.STEP2 = 12                             # Step GPIO Pin
        self.MAGNET = 17                            # Electromagnet relay pin
        self.POWER = 23                             # Relay for turning power on an off to motor controllers to prevent overheating
        self.CW = self.HIGH = GPIO.HIGH             # CLockwise Rotation
        self.CCW = self.LOW =  GPIO.LOW             # Counter Clockwise Rotation
        self.SPR = 400                              # Steps per Rotation (360/1.8)*32
        self.SPS = 434                              # Steps per Chess Square
        self.HALFSPS = 217                          # Steps per half Chess Square
        self.CURRENTX = 0                           # current x position in steps
        self.CURRENTY = 0                           # current y position in steps

        self.direction_xdict = {"negative": GPIO.HIGH, "positive": GPIO.LOW}  # Motors have to turn opposite directions to go positive x and positive y
        self.direction_ydict = {"negative": GPIO.HIGH, "positive": GPIO.LOW}
        self.magnet_dict = {"on":GPIO.HIGH, "off":GPIO.LOW}

        GPIO.setmode(GPIO.BCM)                      # Setup GPIO pins
        GPIO.setup(self.DIR1, GPIO.OUT)
        GPIO.setup(self.STEP1, GPIO.OUT)
        GPIO.setup(self.DIR2, GPIO.OUT)
        GPIO.setup(self.STEP2, GPIO.OUT)
        GPIO.setup(self.MAGNET, GPIO.OUT)
        GPIO.setup(self.POWER, GPIO.OUT)

        self.MODE = (14, 15, 18)                    # Setup for different modes of stepping
        GPIO.setup(self.MODE, GPIO.OUT)             # Specific values for pololu DRV8825 Stepper motor controller
        self.RESOLUTION = {'Full': (self.LOW, self.LOW, self.LOW),
                    'Half': (self.HIGH, self.LOW, self.LOW),
                    '1/4': (self.LOW, self.HIGH, self.LOW),
                    '1/8': (self.HIGH, self.HIGH, self.LOW),
                    '1/16': (self.LOW, self.LOW, self.HIGH),
                    '1/32': (self.HIGH, self.LOW, self.HIGH)}

        GPIO.output(self.MODE, self.RESOLUTION["Half"])    # same speed as full step but much quieter
        self.delay = 0.005 / 16

    def move_stepper1(self, steps):
        '''
        moves x axis stepper in one direction
        '''
        for x in range(steps):
            GPIO.output(self.STEP1, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            sleep(self.delay)

    def move_stepper2(self, steps):
        '''
        moves y axis stepper in one direction
        '''
        for x in range(steps):
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)

    def move_steppers(self, steps):
        '''
        moves both steppers
        '''
        for x in range(steps):
            GPIO.output(self.STEP1, self.HIGH)
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)

    def track_location(self, xSteps, ySteps, xdirection, ydirection):
        '''
        tracks location of electromagnet in steps from (0,0)
        '''
        if xdirection == "positive":
            self.CURRENTX += xSteps
        else:
            self.CURRENTX -= xSteps
        if ydirection == "positive":
            self.CURRENTY += ySteps
        else:
            self.CURRENTY -= ySteps

    def power_on(self):
        '''
        flips relay that controls power to the motor controllers and electromagnet, this prevents the controllers from overheating
        because they stay on to hold motor position
        '''
        GPIO.output(self.POWER, GPIO.HIGH)
        sleep(0.1)

    def power_off(self):
        '''
        flips relay that controls power to the motor controllers and electromagnet, this prevents the controllers from overheating
        because they stay on to hold motor position
        '''
        GPIO.output(self.POWER, GPIO.LOW)
        GPIO.output(self.MAGNET, GPIO.LOW)
        sleep(0.1)

    def queenside_castle(self, color_side):
        self.power_on()
        GPIO.output(self.DIR1, self.direction_xdict["negative"])    # set stepper direction
        if color_side:
            GPIO.output(self.DIR2, self.direction_ydict["positive"])
        else:
            GPIO.output(self.DIR2, self.direction_ydict["negative"])

        GPIO.output(self.MAGNET, self.magnet_dict["on"])            # move king
        self.move_stepper1(self.SPS*2)
        GPIO.output(self.MAGNET, self.magnet_dict["off"])

        self.move_stepper1(self.SPS*2)                              # move rook
        GPIO.output(self.MAGNET, self.magnet_dict["on"])
        self.move_stepper2(self.HALFSPS)

        GPIO.output(self.DIR1, self.direction_xdict["positive"])
        if color_side:
            GPIO.output(self.DIR2, self.direction_ydict["negative"])
        else:
            GPIO.output(self.DIR2, self.direction_ydict["positive"])
        self.move_stepper1(self.SPS*3)
        self.move_stepper2(self.HALFSPS)
        GPIO.output(self.MAGNET, self.magnet_dict["off"])
        self.move_stepper1(self.SPS)
        self.power_off()

    def kingside_castle(self, color_side):
        self.power_on()
        GPIO.output(self.DIR1, self.direction_xdict["positive"])    # set stepper direction
        if color_side:
            GPIO.output(self.DIR2, self.direction_ydict["positive"])
        else:
            GPIO.output(self.DIR2, self.direction_ydict["negative"])

        GPIO.output(self.MAGNET, self.magnet_dict["on"])            # move king
        self.move_stepper1(self.SPS*2)
        GPIO.output(self.MAGNET, self.magnet_dict["off"])

        self.move_stepper1(self.SPS)                                # move rook
        GPIO.output(self.MAGNET, self.magnet_dict["on"])
        self.move_stepper2(self.HALFSPS)

        GPIO.output(self.DIR1, self.direction_xdict["negative"])
        if color_side:
            GPIO.output(self.DIR2, self.direction_ydict["negative"])
        else:
            GPIO.output(self.DIR2, self.direction_ydict["positive"])
        self.move_stepper1(self.SPS*2)
        self.move_stepper2(self.HALFSPS)
        GPIO.output(self.MAGNET, self.magnet_dict["off"])
        self.move_stepper1(self.SPS)                                # move back to king original position
        self.power_off()

    def return_origin(self):
        '''
        moves the electromagnet back to square a1
        '''
        self.move_steps_uneven(self.CURRENTX, self.CURRENTY, "negative", "negative")

    def move_steppers_uneven(self, xSquares, ySquares, xdirection, ydirection, mag, knight):
        '''
        moves electromagnet to squares that are an uneven number of x and y CHESS SQUARES away
        '''
        self.power_on()
        self.track_location(xSquares*self.SPS, ySquares*self.SPS, xdirection, ydirection)

        GPIO.output(self.DIR1, self.direction_xdict[xdirection])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])
        GPIO.output(self.MAGNET, self.magnet_dict[mag])             # set electromagnet position

        if xSquares < ySquares:                       # determines which direction needs to be moved first, moves that direction until both can be moved at once
            squares = xSquares
            squareSteps = squares*self.SPS            # multiplies squares by steps per square to find number of steps
            remain = ySquares - xSquares
            remainSteps = remain*self.SPS
            xfirst = False
        else:
            squares = ySquares
            squareSteps = squares*self.SPS
            remain = xSquares - ySquares
            remainSteps = remain*self.SPS
            xfirst = True

        if xfirst:
            if knight:                              # moves knights on the lines so they dont run into any other pieces
                self.move_stepper2(self.HALFSPS)
                remainSteps += self.HALFSPS
                squareSteps -= self.HALFSPS

            self.move_stepper1(remainSteps)

            #print("movingx" , remainSteps)

        else:
            if knight:
                self.move_stepper1(self.HALFSPS)
                remainSteps += self.HALFSPS
                squareSteps -= self.HALFSPS

            self.move_stepper2(remainSteps)

            #print("movingy" , remainSteps)

        self.move_steppers(squareSteps)

        sleep(0.1)
        self.power_off()

    def move_steps_uneven(self, xSteps, ySteps, xdirection, ydirection):
        '''
        moves electromagnet in an uneven number of x and y STEPS
        '''
        self.power_on()
        self.track_location(xSteps, ySteps, xdirection, ydirection)

        GPIO.output(self.DIR1, self.direction_xdict[xdirection])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        if xSteps < ySteps:                         # determines which direction needs to be moved first, moves that direction until both can be moved at once
            squareSteps = xSteps
            remainSteps = ySteps - xSteps
            xfirst = False
        else:
            squareSteps = ySteps
            remainSteps = xSteps - ySteps
            xfirst = True

        if xfirst:
            #print(remainSteps)
            self.move_stepper1(remainSteps)
        else:
            #print(remainSteps)
            self.move_stepper2(remainSteps)

        #print(squareSteps)
        self.move_steppers(squareSteps)
        self.power_off()

    def take_piece(self, xSquares, ySquares, xdirection, ydirection, move_position):
        '''
        moves pieces off the board that are being taken
        '''
        self.power_on()
        origX = self.CURRENTX                           # saves original piece position so it can be moved back to after taking piece off of board
        origY = self.CURRENTY
        self.track_location(xSquares*self.SPS, ySquares*self.SPS, xdirection, ydirection)

        GPIO.output(self.DIR1, self.direction_xdict[xdirection])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        if xSquares < ySquares:                     # determines which direction needs to be moved first, moves that direction until both can be moved at once
            squares = xSquares
            squareSteps = squares*self.SPS
            remain = ySquares - xSquares
            remainSteps = remain*self.SPS
            #print ("y bigger", remainSteps)
            xfirst = False
        else:
            squares = ySquares
            squareSteps = squares*self.SPS
            remain = xSquares - ySquares
            remainSteps = remain*self.SPS
            #print ("x bigger",remainSteps)
            xfirst = True

        if xfirst:
            self.move_stepper1(remainSteps)

        else:
            self.move_stepper2(remainSteps)

        self.move_steppers(squareSteps)

        GPIO.output(self.DIR1, self.direction_xdict["positive"])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict["negative"])
        GPIO.output(self.MAGNET, self.magnet_dict["on"])            # set electromagnet position

        steps = move_position[1]*self.SPS+self.SPS                  # add one full rotation to get off of the board in the negative y direction
        self.move_stepper1(self.HALFSPS)                            # move piece in the positive x direction to be on the lines
        self.move_stepper2(steps)                                   # takes the piece off of the board
        self.CURRENTX += self.HALFSPS                               # update location
        self.CURRENTY -= steps                                      # update location
        GPIO.output(self.MAGNET, self.magnet_dict["off"])           # turn magnet off


        '''
        moving electromagnet back to original position
        '''
        xSteps = origX - self.CURRENTX                              # finds distance back to original spot
        ySteps = origY - self.CURRENTY
        #print (xSteps, ySteps, self.CURRENTX, self.CURRENTY)
        if xSteps > 0:
            xdirection = "positive"
        else:
            xdirection = "negative"
        if ySteps > 0:
            ydirection = "positive"
        else:
            ydirection = "negative"

        self.move_steps_uneven(abs(xSteps), abs(ySteps), xdirection, ydirection)



        sleep(0.1)
        self.power_off()

'''
# for testing
move = ChessMove()

while (True):
    move.power_on()
    move.kingside_castle()'''

