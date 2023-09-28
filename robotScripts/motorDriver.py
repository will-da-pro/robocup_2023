import RPi.GPIO as GPIO
from time import sleep

class Motors:
    def __init__(self):
        self.in1 = 18 #GPIO pin number
        self.in2 = 24
        self.in3 = 23
        self.in4 = 25

        self.en1 = 12 #the enable pin left
        self.en2 = 16 #the enable pin right

        GPIO.setmode(GPIO.BCM)   #sets pins to outputs
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.setup(self.en1,GPIO.OUT)
        GPIO.setup(self.en2,GPIO.OUT)

        GPIO.output(self.in1,GPIO.LOW) #turns off motors to begin
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

        self.leftPWM = GPIO.PWM(self.en1,1000)
        self.rightPWM = GPIO.PWM(self.en2,1000)
        self.leftPWM.start(0)
        self.rightPWM.start(0)

    def drive(self, speed, turnAngle):
        speed = int(speed)
        turnAngle = int(turnAngle)

        if turnAngle >= 0:
            speedL = speed
            speedR = (-2*turnAngle)+speed
        else:
            speedL = (2*turnAngle)+speed
            speedR = speed
            
        #speedR = -100
        #speedL = 100
            
        #speedR = speedR*-1
        #speedL = speedL*-1

        if speedL > 100:
            speedL = 100
        elif speedL < -100:
            speedL = -100
            
        if speedR > 100:
            speedR = 100
        elif speedR < -100:
            speedR = -100

        absSpeedR = abs(speedL)
        absSpeedL = abs(speedR)

        self.leftPWM.ChangeDutyCycle(absSpeedL)
        self.rightPWM.ChangeDutyCycle(absSpeedR)

        if speedL > 0: #right/backward
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)
        elif speedL < 0: #left/forward
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        else:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.LOW)

        if speedR > 0: #right/forward
            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)
        elif speedR < 0: #left/backward
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
        else: #stop
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)
            
    def forward(self, time, speed):
        GPIO.PWM(self.en1,1000).ChangeDutyCycle(speed)
        GPIO.PWM(self.en2,1000).ChangeDutyCycle(speed)

        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        sleep(time)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

    def backward(self, time, speed):
        GPIO.PWM(self.en1,1000).ChangeDutyCycle(speed)
        GPIO.PWM(self.en2,1000).ChangeDutyCycle(speed)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        sleep(time)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

    def stop(self):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

    def greenLeft():
        Motors(500,-50).moveLeftMotor()
        Motors(500,-50).moveRightMotor()

    def greenRight():
        Motors(500,50).moveRightMotor()
        Motors(500,50).moveLeftMotor()