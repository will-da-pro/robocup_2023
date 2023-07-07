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
        frameWidth = 1920
        
        ret, self.frame = cap.read()
        cv2.resize(self.frame,(679,453))
        self.error = 0

        roi = self.frame[500:600,0:frameWidth]
        
        self.line = cv2.inRange(self.frame,(0,0,0),(40,40,40))
        self.line = cv2.erode(self.line,None,iterations=2)
        self.line = cv2.dilate(self.line,None,iterations=2)
    
        lineContours,_ = cv2.findContours(self.line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(lineContours) > 0:
            largestContour = max(lineContours,key=cv2.contourArea)
            blackbox = cv2.minAreaRect(largestContour)
            (xMin, yMin), (wMin, hMin), self.angle = blackbox
            box = cv2.boxPoints(blackbox)
            box = np.int0(box)
            cv2.drawContours(self.frame,[box],0,(0,255,0),2)
            if self.angle < -45 :
                self.angle = 90 + self.angle
            if wMin < hMin and self.angle > 0:	  
                self.angle = (90-self.angle)*-1
            if wMin > hMin and self.angle < 0:
                self.angle = 90 + self.angle
            #self.angle = abs(self.angle - 90)
            self.error = xMin-(frameWidth/2)
            #cv2.circle(roi,(xMin,300),5,(255,0,0),-1)
            self.angle = (self.angle-90)*-1
        else:
            self.error = 0
            self.angle = 0

        self.angle = int(self.angle)
        self.error = int(self.error)
        
        print("angle = ",self.angle)
        print("error = ",self.error)

        return self.error, self.angle

if __name__ == '__main__':
    follower = LineFollower()
    cap = cv2.VideoCapture(0)
    follower.follow(cap)