#!/usr/bin/python3
import time
from Follower import LineFollower
from motorDriver import Motors
from PidCalc import PID
from checkDistTOF import checkDistance
import cv2
import RPi.GPIO as GPIO

lastError = 0
pastErrors = 0
motorsInit = Motors()
follower = LineFollower()
time.sleep(1) #NESSESARY WHY? IDK BUT IT WORKS maybe it needs to start up bruh idk, it took me too long to work this out
while True:
    #sets distance captured from tof
    lastDistance = distance
    distance = checkDistance()
    if distance is not None:
        print(f"Distance: {distance} mm")
    else:
        print("Error, retrying tho")
        distance = lastDistance

    #error calc
    angle = follower.follow()
    cv2.imshow("frame", follower.frame)
    cv2.imshow("mask", follower.line)
    #pid calc
    pid = PID(angle,1.2,0,0,lastError,pastErrors)
    turnRate = pid.calcTurnRate() 
    #motor output
    motorsInit.drive(100,turnRate)

    #water tower
    #rescue


    if cv2.waitKey(1) & 0xff == ord("s"):
        break
cv2.destroyAllWindows()
GPIO.cleanup()