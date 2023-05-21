from Follower import LineFollower
import motorDriver
from PidCalc import PID

lastError = 0
pastErrors = 0

while True:

    #error calc
    LineFollower.follow()
    error = LineFollower.error

    #pid calc
    PID(error,1,1,1,lastError,pastErrors).calcTurnRate() #change 1's to *'s
    lastError = error
    pastErrors = error + PID.lastError

    #motor output
    




