from Follower import LineFollower
#from motorDriver import Motors
from PidCalc import PID
import cv2

lastError = 0
pastErrors = 0

while True:
    #error calc
    follower = LineFollower()
    error = follower.follow(cv2.VideoCapture(0))
    #pid calc
    print(error)
    turn = PID(error,1,1,1,lastError,pastErrors).calcTurnRate() #change 1's to multipliers
    pastErrors = error + lastError
    lastError = error

    #motor output
    #Motors(500, turn.turnRate).moveLeftMotor()
    #Motors(500, turn.turnRate).moveRightMotor()
    print(turn.turnRate)
    #water tower

    #rescue