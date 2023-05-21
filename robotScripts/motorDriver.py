import RPi.GPIO as GPIO
from time import sleep

class Motors:
    def __init__(self, speed, turnAngle):
        self.speed = speed
        self.turnAngle = turnAngle

        global in1 
        global in2
        global in3
        global in4
        global en1
        global en2

        in1 = 24 #GPIO pin number
        in2 = 23
        in3 = 26
        in4 = 27

        en1 = 25 #the enable pin left
        en2 = 28 #the enable pin right

        GPIO.setmode(GPIO.BCM)   #sets pins to outputs
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(en1,GPIO.OUT)
        GPIO.setup(en2,GPIO.OUT)

        GPIO.output(in1,GPIO.LOW) #turns off motors to begin
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

        #GPIO.PWM(en1,1000)
        #GPIO.PWM(en2,1000)

    def moveLeft(self):
        speedL = (self.speed + self.turnAngle) / 100

        GPIO.PWM(en1,1000).ChangeDutyCycle(speedL)
        
        if speedL > 0: #right/backward
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        elif speedL < 0: #left/forward
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)

    def moveRight(self):
        speedR = (self.speed - self.turnAngle) / 100

        GPIO.PWM(en2,1000).ChangeDutyCycle(speedR)

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