import cv2
import numpy as np

lastError = 0
pastErrors = 0
error = 0
turnRate = 0
cap = cv2.VideoCapture(0)
frameWidth = 256


def calcError():
	global error
	#roi = frame[100:158,0:255]
	lowBlack = np.uint8([30,30,30])#adjust
	highBlack = np.uint8([0,0,0])
	line = cv2.inRange(frame,highBlack,lowBlack)
	
	#line = cv2.GaussianBlur (line, (5,5),0)
	#add erode and dilate
	
	contours,_ = cv2. findContours(line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) > 0:
		largestContour = max(contours,key=cv2.contourArea)
		x,y,w,h = cv2.boundingRect(largestContour)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
		m = cv2.moments(largestContour)
		if m['m00'] > 1:
			x = int(m['m10']/m['m00'])
			y = int(m['m01']/m['m00'])
			error = x-(frameWidth/2)
			print("error = "+str(error))
	else: 
		print("no line")



def calcPID():
	pastErrors = error+lastError
	
	pMult = 1
	iMult = 1
	dMult = 1
	
	pFix = error*pMult
	
	integral = lastError+pastErrors
	iFix = integral*iMult
	
	derivative = error-lastError
	dFix = derivative*dMult
	
	turnRate = (pFix+iFix+dFix)/3
	turnRate = round(turnRate,0)
	print("PID = "+str(turnRate))
	


while True:
	ret,frame = cap.read()
	#frame = cv2.resize(frame,(256,192)) add when on pi
	calcError()
	calcPID()
	#cv2.imshow("Masked",line)
	cv2.imshow("Live",frame)
	lastError = error
	if cv2.waitKey(1) & 0xff == ord("s"):
		break
cap.release()
cv2.destroyAllWindows()