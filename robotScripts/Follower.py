import cv2
import numpy as np
from time import sleep
#from motorDriver import Motors
import warnings
import math

warnings.filterwarnings("ignore")

class LineFollower:
    def __init__(self):
        pass
    
    def follow(self, cap: cv2.VideoCapture) -> None:
        frameWidth = 1358
        
        ret, self.frame = cap.read()
        error = 0

        roi = self.frame[400:500,0:frameWidth]
        green = cv2.inRange(roi,(0,80,0),(70,255,60))
        greenContours,_ = cv2.findContours(green, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        line = cv2.inRange(roi,(0,0,0),(60,60,60))
        #line = cv2.GaussianBlur (line, (5,5),0)
        #add erode and dilate

        if len(greenContours) > 0:
            largestGreenContour = max(greenContours,key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(largestGreenContour)
            cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),5)
            greenDetected = True
        else:
            greenDetected = False
    
        lineContours,_ = cv2.findContours(line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(lineContours) > 0:
            largestContour = max(lineContours,key=cv2.contourArea)
            m = cv2.moments(largestContour)
            if m['m00'] > 0:
                xPos = int(m['m10']/m['m00'])
                yPos = int(m['m01']/m['m00'])
                error = (xPos-(frameWidth/2))/679*100
                cv2.circle(roi,(xPos,yPos),5,(0,0,255),-1)

                cv2.circle(self.frame,(679,906),5,(0,255,0),-1)
                cv2.line(self.frame,(679,906),(xPos,yPos),(0,255,0),2)
                opposite = xPos-679
                adjacent = 906-yPos
                angleRad = math.tan(opposite/adjacent)
                angle = angleRad*(180/3.14159)
                print("angle = ",angle)

        else:
            error = 0


        if greenDetected == True:
            #Motors.stop()
            if error > 0:
                print("greenRight")
            elif error < 0:
                print("greenLeft")
                # Motors.greenLeft()
        print("error = ",error)
        return error

if __name__ == '__main__':
    follower = LineFollower()
    cap = cv2.VideoCapture(0)
    follower.follow(cap)