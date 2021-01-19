from time import sleep
import RPi.GPIO as GPIO


class ChessMove:
    def __init__(self):
        self.DIR1 = 21                              # Directional GPIO Pin
        self.STEP1 = 20                             # Step GPIO Pin
        self.DIR2 = 16                              # Directional GPIO Pin
        self.STEP2 = 12                             # Step GPIO Pin
        self.CW = self.HIGH = GPIO.HIGH        # CLockwise Rotation
        self.CCW = self.LOW =  GPIO.LOW        # Counter Clockwise Rotation
        self.SPR = 6400                             # Steps per Rotation (360/1.8)*32
        self.direction_xdict = {"negative": GPIO.HIGH, "positive": GPIO.LOW}
        self.direction_ydict = {"positive": GPIO.HIGH, "negative": GPIO.LOW}

        GPIO.setmode(GPIO.BCM)                 # Setup GPIO pins
        GPIO.setup(self.DIR1, GPIO.OUT)
        GPIO.setup(self.STEP1, GPIO.OUT)
        GPIO.setup(self.DIR2, GPIO.OUT)
        GPIO.setup(self.STEP2, GPIO.OUT)

        self.MODE = (14, 15, 18)                    # Setup for different modes of stepping
        GPIO.setup(self.MODE, GPIO.OUT)   # Specific values for pololu DRV8825 Stepper motor controller
        self.RESOLUTION = {'Full': (self.LOW, self.LOW, self.LOW),  
                    'Half': (self.HIGH, self.LOW, self.LOW),
                    '1/4': (self.LOW, self.HIGH, self.LOW),
                    '1/8': (self.HIGH, self.HIGH, self.LOW),
                    '1/16': (self.LOW, self.LOW, self.HIGH),
                    '1/32': (self.HIGH, self.LOW, self.HIGH)}

        GPIO.output(self.MODE, self.RESOLUTION["1/32"])    # 6400 steps per revolution
        self.delay = 0.0025 / 32
    
    def move_stepper1(self, steps, direction):
        GPIO.output(self.DIR1, self.direction_xdict[direction])
        for x in range(steps):
            GPIO.output(self.STEP1, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            sleep(self.delay)
    
    def move_stepper2(self, steps, direction):
        GPIO.output(self.DIR2, self.direction_ydict[direction])
        for x in range(steps):
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)
    
    def move_steppers(self, steps, xdirection, ydirection):
        GPIO.output(self.DIR1, self.direction_xdict[xdirection])
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        for x in range(steps):
            GPIO.output(self.STEP1, self.HIGH)
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)
        
    def move_steppers_uneven(self, xSteps, ySteps, xdirection, ydirection):
        GPIO.output(self.DIR1, self.direction_xdict[xdirection])
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

        if xSteps < ySteps:
            steps = xSteps
            remain = ySteps - xSteps
            xfirst = True
        else:
            steps = ySteps
            remain = xSteps - ySteps
            xfirst = False
        
        for x in range(steps):
            GPIO.output(self.STEP1, self.HIGH)
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)

        if xfirst:
            for x in range(remain):
                GPIO.output(self.STEP1, self.HIGH)
                sleep(self.delay)
                GPIO.output(self.STEP1, self.LOW)
                sleep(self.delay)
        else:
            for x in range(remain):
                GPIO.output(self.STEP2, self.HIGH)
                sleep(self.delay)
                GPIO.output(self.STEP2, self.LOW)
                sleep(self.delay)

chess = ChessMove()
for i in range(30):
    chess.move_stepper2(17000, "positive")
    chess.move_stepper2(17000, "negative")

GPIO.cleanup()