import cv2
import numpy as np
from time import sleep
#from motorDriver import Motors
import warnings
import math

class LineFollower:
    def __init__(self):
        pass
    
    def follow(self, cap: cv2.VideoCapture) -> None:
        frameWidth = 1358
        
        ret, self.frame = cap.read()
        cv2.resize(self.frame,(679,453))
        error = 0

        roi = self.frame[500:600,0:frameWidth]
        
        self.line = cv2.inRange(self.frame,(0,0,0),(20,20,20))
        self.line = cv2.erode(self.line,None,iterations=2)
        self.line = cv2.dilate(self.line,None,iterations=2)
        #CHANGE NONE
    
        lineContours,_ = cv2.findContours(self.line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(lineContours) > 0:
            largestContour = max(lineContours,key=cv2.contourArea)
            m = cv2.moments(largestContour)
            if m['m00'] > 0:
                xPos = int(m['m10']/m['m00'])
                yPos = int(m['m01']/m['m00'])
                error = (xPos-(frameWidth/2))/679*100
                cv2.circle(roi,(xPos,yPos),5,(255,0,0),-1)
                cv2.circle(self.frame,(679,906),5,(0,255,0),-1)
                cv2.line(self.frame,(679,906),(xPos,yPos),(0,255,0),2)
                opposite = xPos-679
                adjacent = 906-yPos
                angleRad = math.atan2(opposite, adjacent)
                angle = angleRad*(180/3.14159)
                print("angle = ",angle)
            else:
                angle = 0

        else:
            angle = 0

        return angle 

if __name__ == '__main__':
    follower = LineFollower()
    cap = cv2.VideoCapture(0)
    follower.follow(cap)