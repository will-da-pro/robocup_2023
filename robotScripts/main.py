from Follower import LineFollower
from motorDriver import Motors
from PidCalc import PID
import cv2
from time import sleep

lastError = 0
pastErrors = 0
motorsInit = Motors()
while True:
    #error calc
    follower = LineFollower()
    error = follower.follow(cv2.VideoCapture(0))
    #pid calc
    #print(error)
    pid = PID(error,8,0.5,2,lastError,pastErrors)#change 1's to multipliers
    turnRate = pid.calcTurnRate() 
    pastErrors = error + lastError
    lastError = error
    #print(turnRate)
    #motor output
    motorsInit.drive(100,100)
    sleep(1)
    #water tower

    #rescue