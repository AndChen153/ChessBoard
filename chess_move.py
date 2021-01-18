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
        self.direction_dict = {"positive": GPIO.HIGH, "negative": GPIO.LOW}

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
    
    def move_stepper1(self, steps, dir):
        GPIO.output(self.DIR1, self.direction_dict[dir])
        for x in range(steps):
            GPIO.output(self.STEP1, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            sleep(self.delay)
    
    def move_stepper2(self, steps, dir):
        GPIO.output(self.DIR2, self.direction_dict[dir])
        for x in range(steps):
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)
    
    def move_steppers(self, steps, xdir, ydir):
        GPIO.output(self.DIR1, self.direction_dict[dir])
        GPIO.output(self.DIR2, self.direction_dict[dir])

        for x in range(steps):
            GPIO.output(self.STEP1, self.HIGH)
            GPIO.output(self.STEP2, self.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP1, self.LOW)
            GPIO.output(self.STEP2, self.LOW)
            sleep(self.delay)
        
    '''def stepper_outandside(self, xSteps, ySteps, xDir, yDir):
        global st1
        global st2
        if xdistance < ydistance:
            distance = xdistance
            remain = ydistance - xdistance
            xfirst = True
        else:
            distance = ydistance
            remain = xdistance - ydistance
            xfirst = False
        
        if not st1.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(myStepper1, distance, direction, STEPSTYLE,))
            st1.start()

        if not st2.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(myStepper2, distance, direction, STEPSTYLE,))
            st2.start()

        st1.join()
        st2.join()

        if xfirst and not st1.isAlive():
            st1 = threading.Thread(target=stepper_worker, args=(myStepper1, remain, direction, STEPSTYLE,))
            st1.start()

        if not xfirst and not st2.isAlive():
            st2 = threading.Thread(target=stepper_worker, args=(myStepper2, remain, direction, STEPSTYLE,))
            st2.start()

for x in range(steps):
    self.GPIO.output(self.STEP1, self.HIGH)
    self.GPIO.output(self.STEP2, self.HIGH)
    sleep(delay)
    self.GPIO.output(self.STEP1, self.LOW)
    self.GPIO.output(self.STEP2, self.LOW)
    sleep(delay)
'''

chess = ChessMove()
chess.move_stepper1(19200, "positive")
chess.move_stepper1(19200, "negative")
chess.move_stepper2(19200, "positive")
chess.move_stepper2(19200, "negative")
chess.move_steppers(12800, "positive", "negative")
chess.move_steppers(12800, "positive", "positive")
chess.move_steppers(12800, "negative", "negative")
