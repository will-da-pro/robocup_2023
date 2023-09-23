from Follower import LineFollower
from motorDriver import Motors
from PidCalc import PID
import cv2
import serial
import time

lastError = 0
pastErrors = 0
motorsInit = Motors()
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



    #motor output
    ser = serial.Serial('/dev/ttyUSB0', 9600)

    def send_command(command, speed=None, turn_angle=None):
        if speed is not None:
            command += f" {speed}"
        if turn_angle is not None:
            command += f" {turn_angle}"
        
        ser.write(command.encode('utf-8') + b'\n')
        response = ser.readline().decode('utf-8').strip()
        return response

    # Example commands to send to Arduino
    comStop = "pls stop"
    stopRes = send_command(comStop)
    print("Stop Response:", stopRes)

    comDrive = "pls drive"
    driveRes = send_command(comDrive, 50, turnRate) #middle term is speed
    print("Drive Response:", driveRes)



    #water tower
    #rescue
    if cv2.waitKey(1) & 0xff == ord("s"):
        break
cap.release()
cv2.destroyAllWindows()
ser.close()