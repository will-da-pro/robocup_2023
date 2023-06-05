import cv2
import numpy as np
from time import sleep
#from motorDriver import Motors
import warnings
import time

start_time = [None]

def stopwatch_start():
    start_time[0] = time.time()

def stopwatch_stop():
    execution_time = time.time() - start_time[0]
    start_time[0] = None
    return execution_time

warnings.filterwarnings("ignore")

class LineFollower:
    def __init__(self):
        pass
    
    def follow(self, cap: cv2.VideoCapture) -> None:
        ###
        frameWidth = 1358
        
        ret, frame = cap.read()
        self.error = 0

        ###0.22 seconds

        #roi = frame[100:158,0:255]
        green = cv2.inRange(frame,(0,80,0),(70,255,60))
        greenContours,_ = cv2.findContours(green, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        line = cv2.inRange(frame,(0,0,0),(40,40,40))
        #line = cv2.GaussianBlur (line, (5,5),0)
        #add erode and dilate

        if len(greenContours) > 0:
            largestGreenContour = max(greenContours,key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(largestGreenContour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
            greenDetected = True
        else:
            greenDetected = False
    
        lineContours,_ = cv2.findContours(line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(lineContours) == 0:
            print("no line")
            error = 0
        else:
            largestContour = max(lineContours,key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(largestContour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
            m = cv2.moments(largestContour)

        if m['m00'] > 1:
            x = int(m['m10']/m['m00'])
            y = int(m['m01']/m['m00'])
            error = (x-(frameWidth/2))/679*100
            print("error = "+str(error))
            cv2.circle(frame,(x,y),5,(0,0,255),-1)
        else:
            error = 0
        if greenDetected == True:
            #Motors.stop()
            if error > 0:
                print("greenRight")
                #Motors.greenRight()
            elif error < 0:
                print("greenLeft")
                # Motors.greenLeft()
            
        return error

if __name__ == '__main__':
    follower = LineFollower()
    stopwatch_start()
    cap = cv2.VideoCapture(0)
    time = stopwatch_stop()
    print(f"Execution time: {time:.2f} seconds")
    follower.follow(cap)