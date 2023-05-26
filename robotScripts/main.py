from Follower import LineFollower
#from motorDriver import Motors
from PidCalc import PID
import cv2

lastError = 0
pastErrors = 0

while True:
    #error calc
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    follower = LineFollower()
    if ret:
        cv2.imshow('a frame', frame)
        error = follower.follow(frame)
        #pid calc
        turn = PID(error,1,1,1,lastError,pastErrors).calcTurnRate() #change 1's to multipliers
        pastErrors = error + lastError
        lastError = error

        #motor output
        #Motors(500, turn.turnRate).moveLeftMotor()
        #Motors(500, turn.turnRate).moveRightMotor()
        print(turn)
        #water tower

        #rescue
    else:
        break