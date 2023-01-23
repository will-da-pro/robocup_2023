import cv2
import numpy as np
cap = cv2.VideoCapture (0)
while True:
	ret,frame = cap.read()
	frame = cv2. resize frame, (256, 192))
	#roi = frame 100:158, 0:255]
	lowBlack = np.uint8([30,30,30])
	highBlack = np.uint8([0,0,0])
	line = cv2.inRange(frame,highBlack,lowBlack)
	highBlack = np.uint8([0,0,0])
	line = cv2.inRange (frame, highBlack, lowBlack)
	line = cv2.GaussianBlur (line, (5,5),0)
	#add erode and dilate
	contours,_ = cv2. findContours (line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	if len (contours) > 0:
		largestContour = max(contours, key=v2.contourArea)
		x,y,w,h = cv2.boundingRect (largestContour)
		cv2. rectangle(frame, (x,y), (x+w, y+h) , (0,255,0),2)
		m = cv2.moments (largestContour)
		x = int (m['m10']/m['m00'])
		y = int (m['m01']/m['m00'])
		error = x-128
		print (error)
	else:
		print ("no line")
	cv2.imshow("Masked", line) cv2.imshow ("Live", frame)
	if cv2.waitKey(1) & Oxff == ord("s"):
		break
cap.release()
cv2. destroyAllWindows()

return error
