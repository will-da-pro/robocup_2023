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
        self.error = 0

        roi = self.frame[800:906,0:frameWidth]
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
            x,y,w,h = cv2.boundingRect(largestContour)
            cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),5)

            m = cv2.moments(largestContour)
            if m['m00'] > 1:
                xPos = int(m['m10']/m['m00'])
                yPos = int(m['m01']/m['m00'])
                error = (xPos-(frameWidth/2))/679*100
            else:
                error = 0
            print("error = "+str(error))
            cv2.circle(roi,(xPos,yPos),5,(0,0,255),-1)

            


        if greenDetected == True:
            #Motors.stop()
            if error > 0:
                print("greenRight")
            elif error < 0:
                print("greenLeft")
                # Motors.greenLeft()

        return error

if __name__ == '__main__':
    follower = LineFollower()
    cap = cv2.VideoCapture(0)
    follower.follow(cap)