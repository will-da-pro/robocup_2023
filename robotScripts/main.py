from Follower import LineFollower
#from motorDriver import Motors
from PidCalc import PID
import cv2

lastError = 0
pastErrors = 0
#motorsInit = Motors()
cap = cv2.VideoCapture(0)
while True:
    #error calc
    follower = LineFollower()
    error = follower.follow(cap)
    #pid calc
    #print(error)
    pid = PID(error,2,0.05,0.2,lastError,pastErrors)#change 1's to multipliers
    turnRate = pid.calcTurnRate() 
    pastErrors = error + lastError
    lastError = error
    #print(turnRate)
    #motor output
    #motorsInit.drive(100,100)
    #sleep(1)
    #water tower

    #rescue