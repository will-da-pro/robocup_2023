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
        cv2.resize(self.frame,(679,453))
        self.error = 0

        roi = self.frame[500:600,0:frameWidth]
        
        self.line = cv2.inRange(self.frame,(0,0,0),(20,20,20))
        self.line = cv2.erode(self.line,None,iterations=2)
        self.line = cv2.dilate(self.line,None,iterations=2)
    
        lineContours,_ = cv2.findContours(self.line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(lineContours) > 0:
            largestContour = max(lineContours,key=cv2.contourArea)
            blackbox = cv2.minAreaRect(largestContour[0])
            (xMin, yMin), (wMin, hMin), self.angle = blackbox
            if self.angle < -45 :
                self.angle = 90 + self.angle
            if wMin < hMin and self.angle > 0:	  
                self.angle = (90-self.angle)*-1
            if wMin > hMin and self.angle < 0:
                self.angle = 90 + self.angle
            
            self.error = (xMin-(frameWidth/2))/679*100
            cv2.circle(roi,(xMin,300),5,(255,0,0),-1)
        else:
            self.error = 0
            self.angle = 0

        print("angle = ",self.angle)
        print("error = ",self.error)

if __name__ == '__main__':
    follower = LineFollower()
    cap = cv2.VideoCapture(0)
    follower.follow(cap)