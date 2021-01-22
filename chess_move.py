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
        #self.SPR = 400*2                            # Steps per Rotation (360/1.8)*32
        #self.SPS = 434*2                            # Steps per Chess Square
        #self.HALFSPS = 217*2                        # Steps per half Chess Square
        self.SPR = 400                            # Steps per Rotation (360/1.8)*32
        self.SPS = 434                            # Steps per Chess Square
        self.HALFSPS = 217                        # Steps per half Chess Square
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
        self.delay = 0.0025 / 32
    
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
        if xdirection == "positive":
            self.CURRENTX += xSteps
        else:
            self.CURRENTX -= xSteps
        if ydirection == "positive":
            self.CURRENTY += ySteps
        else:
            self.CURRENTY -= ySteps

    def power_on(self):
        GPIO.output(self.POWER, GPIO.HIGH)
        sleep(0.1)

    def move_steppers_uneven(self, xSquares, ySquares, xdirection, ydirection, mag, knight):
        self.power_on()
        self.track_location(xSquares*self.SPS, ySquares*self.SPS, xdirection, ydirection)

        GPIO.output(self.DIR1, self.direction_xdict[xdirection])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])
        GPIO.output(self.MAGNET, self.magnet_dict[mag])             # set electromagnet position

        if xSquares < ySquares:
            squares = xSquares
            squareSteps = squares*self.SPS
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
            if knight:
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
        GPIO.output(self.MAGNET, GPIO.LOW)
        GPIO.output(self.POWER, GPIO.LOW)

    def move_steps_uneven(self, xSteps, ySteps, xdirection, ydirection):
        self.power_on()
        self.track_location(xSteps, ySteps, xdirection, ydirection)

        GPIO.output(self.DIR1, self.direction_xdict[xdirection])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        if xSteps < ySteps:
            squareSteps = xSteps
            remainSteps = ySteps - xSteps
            xfirst = False
        else:
            squareSteps = ySteps
            remainSteps = xSteps - ySteps
            xfirst = True
            
        if xfirst:
            print(remainSteps)
            self.move_stepper1(remainSteps)
        else:
            print(remainSteps)
            self.move_stepper2(remainSteps)
        
        print(squareSteps)
        self.move_steppers(squareSteps)
        
        sleep(0.1)
        GPIO.output(self.POWER, GPIO.LOW)

    def take_piece(self, xSquares, ySquares, xdirection, ydirection, move_position):
        self.power_on()
        origX = self.CURRENTX
        origY = self.CURRENTY
        self.track_location(xSquares*self.SPS, ySquares*self.SPS, xdirection, ydirection)

        GPIO.output(self.DIR1, self.direction_xdict[xdirection])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        if xSquares < ySquares:
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

        steps = move_position[1]*self.SPS+self.SPR
        self.move_stepper1(self.HALFSPS)
        self.move_stepper2(steps)
        self.CURRENTX += self.HALFSPS                               # update location
        self.CURRENTY -= steps                                      # update location
        GPIO.output(self.MAGNET, self.magnet_dict["off"])

        xSteps = origX - self.CURRENTX
        ySteps = origY - self.CURRENTY
        print (xSteps, ySteps, self.CURRENTX, self.CURRENTY)
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
        GPIO.output(self.POWER, GPIO.LOW)

'''
move = ChessMove()

while (True):
    move.power_on()
    x = int(input())    # 1
    y = int(input())    # 0
    move.move_steppers_uneven(x,y,"positive","positive","off",False)'''

