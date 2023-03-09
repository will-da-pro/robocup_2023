import cv2
import numpy as np

lastError = 0
pastErrors = 0
error = 0
turnRate = 0

cap = cv2.VideoCapture(0)
frameWidth = 1920
frameHeight = 1080

def calcError():
	global error
	global line

	#roi = frame[0:100,0:frameWidth]#hash and change roi to frame
	lowBlack = np.uint8([50,50,50])#adjust
	highBlack = np.uint8([0,0,0])

	line = cv2.inRange(frame,highBlack,lowBlack)
	kernel = np.ones((3,3), np.uint8)
	line = cv2.erode(line, kernel, iterations=5)
	line = cv2.dilate(line, kernel, iterations=9)
	#blur	
	
	contours,_ = cv2. findContours(line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) > 0:
		largestContour = max(contours,key=cv2.contourArea)
		x,y,w,h = cv2.boundingRect(largestContour)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
		center = ((x+(x+w))/2)
		error = center-(frameWidth/2)
		print("Error = "+str(error))



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
	
	print(pFix)
	print(iFix)
	print(dFix)

	turnRate = (pFix+iFix+dFix)/3
	turnRate = round(turnRate,0)
	print("PID = "+str(turnRate))
	


while True:
	ret,frame = cap.read()
	frame = cv2.resize(frame,(frameWidth,frameHeight)) #if error here then width/height incorrect
	calcError()
	calcPID()
	cv2.imshow("Masked",line)
	#cv2.imshow("Live",frame)
	lastError = error
	if cv2.waitKey(1) & 0xff == ord("s"):
		break
cap.release()
cv2.destroyAllWindows()