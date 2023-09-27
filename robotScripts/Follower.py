import cv2
import numpy as np
from time import sleep
from piCam import PiVideoStream
#from motorDriver import Motors
import warnings
import math


class LineFollower:
    def __init__(self):
        global stream
        stream = PiVideoStream()
        stream.start()
    
    def follow(self) -> None:
        frameWidth = 480
        frameHeight = 240
        halfFrameWidth = 240
        halfFrameHeight = 120
        
        self.frame = stream.read()
        
        self.frame = cv2.flip(self.frame, 0)

        #roi = self.frame[100:200,0:frameWidth] not being used rn
        
        self.line = cv2.inRange(self.frame,(0,0,0),(20,20,20))
        self.line = cv2.GaussianBlur(self.line,(5,5),0)
        kernel = np.ones((3,3), np.uint8)
        self.line = cv2.erode(self.line, kernel, iterations=3)
        #self.line = cv2.dilate(self.line,kernel,iterations=2) idk reilly doesnt have it
    
        #lineContours,_ = cv2.findContours(self.line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(self.line) > 100:
            #largestContour = max(lineContours,key=cv2.contourArea)
            m = cv2.moments(self.line)
            if m['m00'] > 0:
                xPos = int(m['m10']/m['m00'])
                yPos = int(m['m01']/m['m00'])
                cv2.circle(self.frame,(xPos,yPos),5,(255,0,0),-1)
                cv2.circle(self.frame,(halfFrameWidth,halfFrameWidth),5,(0,255,0),-1)
                cv2.line(self.frame,(halfFrameWidth,halfFrameWidth),(xPos,yPos),(0,255,0),2)
                opposite = halfFrameWidth-xPos
                adjacent = frameHeight-yPos
                angleRad = math.atan2(opposite,adjacent)
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
    follower.follow()