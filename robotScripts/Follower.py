import cv2
import numpy as np

class LineFollower:
    def __init__(self):
        pass
    
    def follow(self, cap: cv2.VideoCapture) -> None:
        frameWidth = 256
        while True:
            ret, frame = cap.read()
            global error
            #roi = frame[100:158,0:255]
            lowBlack = np.uint8([30,30,30])#adjust
            highBlack = np.uint8([0,0,0])
            line = cv2.inRange(frame,highBlack,lowBlack)
    
            #line = cv2.GaussianBlur (line, (5,5),0)
            #add erode and dilate
    
            contours,_ = cv2. findContours(line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) == 0:
                print("no line")
            
            largestContour = max(contours,key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(largestContour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
            m = cv2.moments(largestContour)
            
            if m['m00'] > 1:
                x = int(m['m10']/m['m00'])
                y = int(m['m01']/m['m00'])
                error = x-(frameWidth/2)
                print("error = "+str(error))
                cv2.circle(frame,(x,y),5,(0,0,255),-1)
            cv2.imshow('img', frame)


if __name__ == '__main__':
    follower = LineFollower()
    cap = cv2.VideoCapture(0)
    follower.follow(cap)