import cv2
import numpy as np
#from motorDriver import Motors

class LineFollower:
    def __init__(self):
        pass
    
    def follow(self, cap: cv2.VideoCapture) -> None:
        frameWidth = 1080
        while True:
            ret, frame = cap.read()
            global error
            
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
            else:
                largestContour = max(lineContours,key=cv2.contourArea)
                x,y,w,h = cv2.boundingRect(largestContour)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
                m = cv2.moments(largestContour)

            if m['m00'] > 1:
                x = int(m['m10']/m['m00'])
                y = int(m['m01']/m['m00'])
                error = x-(frameWidth/2)
                error -= 99
                print("error = "+str(error))
                cv2.circle(frame,(x,y),5,(0,0,255),-1)
            
            if greenDetected == True:
                #Motors.stop()
                if error > 0:
                    print("greenRight")
                    #Motors.greenRight()
                elif error < 0:
                    print("greenLeft")
                    #Motors.greenLeft()
            
            cv2.imshow('a frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    follower = LineFollower()
    cap = cv2.VideoCapture(0)
    follower.follow(cap)