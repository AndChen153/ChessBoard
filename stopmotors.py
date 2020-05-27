from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor



mh = Adafruit_MotorHAT()


mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)