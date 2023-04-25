import RPi.GPIO as GPIO

class Motors:
    def __init__(self, direction, speedL, speedR):
        self.direction = direction
        self.speedL = speedL
        self.speedR = speedR

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

        GPIO.PWM(en1,1000)
        GPIO.PWM(en2,1000)

    def moveLeft(self):
        GPIO.PWM(en1,1000).ChangeDutyCycle(self.speedL) #sets speed - self.speed must be 0-100

        if self.direction == 1: #turns the motor forward
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        elif self.direction == 2: #turns the motor backward
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
        else:
            print("ERROR moveLeft: First argument (Direction) takes '1'-Forward OR '2'-Backward")

    def moveRight(self):
        GPIO.PWM(en2,1000).ChangeDutyCycle(self.speedR) 

        if self.direction == 1:
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
        elif self.direction == 2:
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
        else:
            print("ERROR moveLeft: First argument (Direction) takes either '1'-Forward OR '2'-Backward")