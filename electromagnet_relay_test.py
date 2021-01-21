import RPi.GPIO as GPIO
import time

channel = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


while True:
    y=input("a or b")

    if y == "a":
        GPIO.output(channel, GPIO.HIGH)
        

    elif y == "b":
        GPIO.output(channel, GPIO.LOW)

GPIO.cleanup()


def take_piece(self, xSquares, ySquares, xdirection, ydirection, move_position):
        GPIO.output(self.DIR1, self.direction_xdict[xdirection])    # set stepper direction
        GPIO.output(self.DIR2, self.direction_ydict[ydirection])

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
            self.move_stepper1(remainSteps)

        else:
            self.move_stepper2(remainSteps)
        
        self.move_steppers(squareSteps)
        
        if move_position[0] == 7:
            GPIO.output(self.DIR1, self.direction_xdict["negative"])    # set stepper direction
            return_dir = "positive"
        else:
            GPIO.output(self.DIR1, self.direction_xdict["positive"])    # set stepper direction
            return_dir = "negative"
        GPIO.output(self.DIR2, self.direction_ydict["negative"])
        GPIO.output(self.MAGNET, self.magnet_dict["on"])             # set electromagnet position

        steps = move_position[1]*self.SPS+self.SPR
        self.move_stepper1(self.HALFSPS)
        self.move_stepper2(steps)
        GPIO.output(self.MAGNET, GPIO.LOW)


        GPIO.output(self.DIR1, self.direction_xdict[return_dir])  
        GPIO.output(self.DIR2, self.direction_ydict["positive"])
        if xfirst:
            self.move_stepper1(remainSteps+self.HALFSPS)
        else:
            self.move_stepper2(steps-remainSteps-self.SPR)
        
        self.move_steppers(squareSteps)

        sleep(0.5)
        GPIO.output(self.POWER, GPIO.LOW)
