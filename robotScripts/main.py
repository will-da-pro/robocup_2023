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
distance = 0
motors = Motors()
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
    #cv2.imshow("grey", follower.grey)
    #pid calc
    pid = PID(angle,2.1,0,0,lastError,pastErrors)
    turnRate = pid.calcTurnRate() 
    #motor output
    motors.drive(100,turnRate)

    #water tower
    if distance < 100:
        time.sleep(0.1)
        lastDistance = distance
        distance = checkDistance()
        if distance is not None:
            print(f"Distance: {distance} mm")
        else:
            print("Error, retrying tho")
            distance = lastDistance
        if distance < 100: #double check, robot may be tripping
            print(f"water tower @ {distance}")
            motors.stop()
            time.sleep(1)
            
            #motors.backward(1,50)#backward
            #time.sleep(1)
            #motors.stop()
            #time.sleep(5)
            
            motors.drive(5,100) #rotate on the spot
            time.sleep(0.5)
            motors.stop()
            time.sleep(2)
            
            motors.drive(100,-38)
            time.sleep(3.5)
            #while follower.lineInFrame() == False:
            #    motors.drive(50,-20) #around tower
            motors.stop()
            time.sleep(5)
            
            #motors.drive(20,100)
            #time.sleep(0.1)
            #motors.stop()

    #rescue
    isSilver = follower.checkSilver()
    if isSilver == True:
        motors.stop()
        time.sleep(2)
        isSilver = follower.checkSilver()
        if isSilver == True: 
            print(f"THERES RESCUE TILE with {isSilver} silver")
            motors.drive(50,0)
            time.sleep(2)
            motors.stop() #move to middle
            time.sleep(0)
            
            motors.drive(100,-100)
            time.sleep(1)
            motors.stop() #turn to starting pos
            time.sleep(0.5)
            
            motors.drive(100,100)
            distance = 1000
            while True:
                timeout_seconds = 30  # Adjust the overall search duration as needed
                check_interval = 0.5  # Adjust the interval between distance checks as needed
                start_time = time.time()

                while time.time() - start_time < timeout_seconds:
                    distances = []
                    while time.time() - start_time < check_interval:
                        distance = checkDistance()
                        if distance is not None:
                            distances.append(distance)
        
                if distances:
                    avg_distance = sum(distances) / len(distances)
                    print(f"Avg Distance: {avg_distance} mm")
                    if avg_distance < 200:
                        print("Object detected within 200 mm, stopping.")
                        MOVEHERE
                    else:
                        print("no can found, still searching")
                else:
                    print("error from i2c")

    print("can was a ghost")


    if cv2.waitKey(1) & 0xff == ord("s"):
        break
cv2.destroyAllWindows()
GPIO.cleanup()


