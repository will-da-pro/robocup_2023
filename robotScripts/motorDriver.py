import RPi.GPIO as GPIO
from time import sleep

class Motors:
    def __init__(self):

        global in1 
        global in2
        global in3
        global in4
        global en1
        global en2

        in1 = 25 #GPIO pin number
        in2 = 24
        in3 = 23
        in4 = 18

        en1 = 12 #the enable pin left
        en2 = 16 #the enable pin right

        GPIO.setmode(GPIO.BCM)   #sets pins to outputs
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(in3,GPIO.OUT)
        GPIO.setup(in4,GPIO.OUT)
        GPIO.setup(en1,GPIO.OUT)
        GPIO.setup(en2,GPIO.OUT)

        GPIO.output(in1,GPIO.LOW) #turns off motors to begin
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

        self.leftPWM = GPIO.PWM(en1,1000)
        self.rightPWM = GPIO.PWM(en2,1000)
        self.leftPWM.start(0)
        self.rightPWM.start(0)

    def drive(self, speed, turnAngle):
        speed = int(speed)
        turnAngle = int(turnAngle)

        speedL = (speed + turnAngle) / 100
        speedR = (speed - turnAngle) / 100

        self.leftPWM.ChangeDutyCycle(speedL)
        self.leftPWM.ChangeDutyCycle(speedR)

        if speedL > 0: #right/backward
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
        elif speedL < 0: #left/forward
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)

        if speedR > 0: #right/forward
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
        elif speedR < 0: #left/backward
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
        else: #stop
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)

    def forward(self, time, speed):
        GPIO.PWM(en1,1000).ChangeDutyCycle(speed)
        GPIO.PWM(en2,1000).ChangeDutyCycle(speed)

        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        sleep(time)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

    def backward(self, time, speed):
        GPIO.PWM(en1,1000).ChangeDutyCycle(speed)
        GPIO.PWM(en2,1000).ChangeDutyCycle(speed)

        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(time)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

    def stop(self):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

    def greenLeft():
        Motors(500,-50).moveLeftMotor()
        Motors(500,-50).moveRightMotor()

    def greenRight():
        Motors(500,50).moveRightMotor()
        Motors(500,50).moveLeftMotor()