from adafruit_motorkit import Motorkit
from adafruit_motor import stepper
kit = Motorkit()

for i in range (20):
    kit.stepper1.onestep()
for i in range (20):
    kit.stepper2.onestep()