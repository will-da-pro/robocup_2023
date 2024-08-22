import numpy as np
import cv2, queue, threading
import math
#from drive import driveBase

# bufferless VideoCapture
class VideoCapture:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

#robot = driveBase(29, 31, 33, 35)
cap = VideoCapture(1)
while True:
    frame = cap.read()
    frame = cv2.flip(frame, 1, frame)
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.bitwise_not(imgray)
    ret, thresh = cv2.threshold(imgray, 120, 255, 0)
    #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = np.copy(frame)
    imgThirdSize = int(len(thresh[0])/3)

    #Get Line
    r = 400
    angle = 0
  
    originx = int(len(thresh[0])/2)
    originy = 900
  
    linePos = []
    lineCentreArray = []
    startLine = 0
    isLine = False
  
    while angle <= 180:
        x = originx - int(r * math.cos(angle * math.pi / 180))
        y = originy - int(r * math.sin(angle * math.pi / 180))
      
        #print(angle, originx, x, y)
      
        val = thresh[y][x]
        
        if val == 255:
            if not isLine:
                startLine = angle
                isLine = True
            elif angle == 180:
                linePos.append([startLine, angle])
                isLine = False
            img = cv2.circle(img, (x, y), 0, (0,255,0), 5)
        else:
            if isLine:
                linePos.append([startLine, angle])
                isLine = False
            img = cv2.circle(img, (x, y), 0, (255,0,0), 5)
            
        angle += 1
    
    for i in linePos:
        centre = np.average(i)
        
        x = originx - int(r * math.cos(centre * math.pi / 180))
        y = originy - int(r * math.sin(centre * math.pi / 180))
        
        img = cv2.circle(img, (x, y), 0, (0,0,255), 20)
        
        lineCentreArray.append(centre)
        
  
    #green square
    landon2 = 0
    n = imgThirdSize
    greenVal = 0
    greenPos = 900
    while n < (imgThirdSize * 2):
        if img[greenPos][n][1] >= img[greenPos][n][0] + 20 and img[greenPos][n][1] >= img[greenPos][n][2] + 20:
            greenVal += n
            landon2 += 1
        n += 1
    if landon2 > 0:
        greenVal /= landon2
        greenVal = int(greenVal)
    else:
        greenVal = None
        n += 1
        
    lineCount = len(lineCentreArray)
    targetAngle = 90
    
    if lineCount == 0:
        targetAngle = 90
    elif lineCount == 1:
        targetAngle = lineCentreArray[0]
    else:
        if greenVal == None:
            closestVal = lineCentreArray[0] - 90
            for i in lineCentreArray:
                if abs(closestVal) - abs(i - 90) > 0:
                    closestVal = i - 90
            targetAngle = closestVal + 90
        elif greenVal < len(frame[0]) / 2:
            targetAngle = lineCentreArray[0]
        else:
            targetAngle = lineCentreArray[len(lineCentreArray) - 1]
            
    img = cv2.line(img, (originx, originy), (originx - int(r * math.cos(targetAngle * math.pi / 180)), originy - int(r * math.sin(targetAngle * math.pi / 180))), (255, 0, 255), 5)

    turnVal = (targetAngle - 90) / 90
    #robot.drive(60, turnVal)

    #cv2.drawContours(img, contours, -1, (0,0,255), 3)
    img = cv2.line(img, (0, greenPos), (len(thresh[0]), greenPos), (0, 0, 255), 3)
    if greenVal != None:
        img = cv2.circle(img, (greenVal, greenPos), 10, (255, 0, 0), 5)
  
    cv2.imshow("frame", img)
    if chr(cv2.waitKey(1)&255) == 'q':
        break