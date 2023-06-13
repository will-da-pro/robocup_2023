from Follower import LineFollower
from motorDriver import Motors
from PidCalc import PID
import cv2

lastError = 0
pastErrors = 0
motorsInit = Motors()
cap = cv2.VideoCapture(0)
while True:
    #error calc
    follower = LineFollower()
    error = follower.follow(cap)
    cv2.imshow("frame", follower.frame)
    #pid calc
    pid = PID(error,2,0.05,0.2,lastError,pastErrors)#change 1's to multipliers
    turnRate = pid.calcTurnRate() 
    print(turnRate)
    #motor output
    motorsInit.drive(75,turnRate)
    #water tower

    #rescue
    if cv2.waitKey(1) & 0xff == ord("s"):
        break
cap.release()
cv2.destroyAllWindows()