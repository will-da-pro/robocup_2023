from Follower import LineFollower
from motorDriver import Motors
from PidCalc import PID

lastError = 0
pastErrors = 0

while True:
    #error calc
    LineFollower.follow()
    error = LineFollower.error

    #pid calc
    PID(error,1,1,1,lastError,pastErrors).calcTurnRate() #change 1's to multipliers
    pastErrors = error + lastError
    lastError = error

    #motor output
    Motors(500, PID.turnRate).moveLeftMotor()
    Motors(500, PID.turnRate).moveRightMotor()

    #water tower

    #rescue