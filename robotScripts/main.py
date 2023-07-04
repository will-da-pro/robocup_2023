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
    angle = follower.follow(cap)
    cv2.imshow("frame", follower.frame)
    cv2.imshow("mask", follower.line)
    #pid calc
    pid = PID(angle,3,0,0,lastError,pastErrors)
    turnRate = pid.calcTurnRate() 
    #print(turnRate)
    #motor output
    #motorsInit.drive(75,turnRate)
    #water tower

    #rescue
    if cv2.waitKey(1) & 0xff == ord("s"):
        break
cap.release()
cv2.destroyAllWindows()