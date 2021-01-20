from time import sleep
import RPi.GPIO as GPIO

# 7000 steps per block

class ChessMove:
    def __init__(self):
        self.DIR1 = 21                              # Directional GPIO Pin
        self.STEP1 = 20                             # Step GPIO Pin
        self.DIR2 = 16                              # Directional GPIO Pin
        self.STEP2 = 12                             # Step GPIO Pin
        self.CW = self.HIGH = GPIO.HIGH             # CLockwise Rotation
        self.CCW = self.LOW =  GPIO.LOW             # Counter Clockwise Rotation
        self.SPR = 6400                             # Steps per Rotation (360/1.8)*32
        self.SPS = 7000                             # Steps per Chess Square

        self.direction_xdict = {"positive": GPIO.HIGH, "negative": GPIO.LOW}
        self.direction_ydict = {"negative": GPIO.HIGH, "positive": GPIO.LOW}

        GPIO.setmode(GPIO.BCM)                 # Setup GPIO pins
        GPIO.setup(self.DIR1, GPIO.OUT)
        GPIO.setup(self.STEP1, GPIO.OUT)
        GPIO.setup(self.DIR2, GPIO.OUT)
        GPIO.setup(self.STEP2, GPIO.OUT)

        self.MODE = (14, 15, 18)                    # Setup for different modes of stepping
        GPIO.setup(self.MODE, GPIO.OUT)             # Specific values for pololu DRV8825 Stepper motor controller
        self.RESOLUTION = {'Full': (self.LOW, self.LOW, self.LOW),  
                    'Half': (self.HIGH, self.LOW, self.LOW),
                    '1/4': (self.LOW, self.HIGH, self.LOW),
                    '1/8': (self.HIGH, self.HIGH, self.LOW),
                    '1/16': (self.LOW, self.LOW, self.HIGH),
                    '1/32': (self.HIGH, self.LOW, self.HIGH)}

        GPIO.output(self.MODE, self.RESOLUTION["1/32"])    # same speed as full step but much quieter
        self.delay = 0.0025 / 32
    
    def move_stepper1(self, squares, direction):
        '''
        moves x axis stepper in one direction
        '''
        GPIO.output(self.DIR1, self.direction_xdict[direction])     #set direction of drive
        for x in range(squares*self.SPS):
            GPIO.output(self.STEP1, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            sleep(self.delay)
    
    def move_stepper2(self, squares, direction):
        '''
        moves y axis stepper in one direction
        '''
        GPIO.output(self.DIR2, self.direction_ydict[direction])
        for x in range(squares*self.SPS):
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)
    
    def move_steppers(self, squares, xdirection, ydirection):
        '''
        moves both steppers in same or separate directions
        '''

        GPIO.output(self.DIR1, self.direction_xdict[xdirection])
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        for x in range(squares*self.SPS):
            GPIO.output(self.STEP1, self.HIGH)
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)
        
    def move_steppers_uneven(self, xSquares, ySquares, xdirection, ydirection):
        GPIO.output(self.DIR1, self.direction_xdict[xdirection])
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        if xSquares < ySquares:
            squares = xSquares
            remain = ySquares - xSquares
            xfirst = True
        else:
            squares = ySquares
            remain = xSquares - ySquares
            xfirst = False
        
        for x in range(squares*self.SPS):
            GPIO.output(self.STEP1, self.HIGH)
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)

        if xfirst:
            for x in range(remain*self.SPS):
                GPIO.output(self.STEP1, self.HIGH)
                sleep(self.delay)
                GPIO.output(self.STEP1, self.LOW)
                sleep(self.delay)
        else:
            for x in range(remain*self.SPS):
                GPIO.output(self.STEP2, self.HIGH)
                sleep(self.delay)
                GPIO.output(self.STEP2, self.LOW)
                sleep(self.delay)
