import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from time import sleep
#from motorDriver import Motors
import warnings
import math

class PiVideoStream:
	def __init__(self, resolution=(480, 240), framerate=41, **kwargs):
		# initialize the camera
		self.camera = PiCamera()

		# set camera parameters
		self.camera.resolution = resolution #480x240
		self.camera.framerate = framerate
		self.camera.sensor_mode = 6
		self.camera.shutter_speed = 7000
		self.camera.exposure_mode = 'off'
		
		# set optional camera parameters (refer to PiCamera docs)
		for (arg, value) in kwargs.items():
			setattr(self.camera, arg, value)

		# initialize the stream
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array
			self.rawCapture.truncate(0)

			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

class LineFollower:
    def __init__(self):
        pass
    
    def follow(self, cap: cv2.VideoCapture) -> None:
        frameWidth = 1358
        
        ret, self.frame = cap.read()
        cv2.resize(self.frame,(679,453))
        error = 0

        roi = self.frame[500:600,0:frameWidth]
        
        self.line = cv2.inRange(self.frame,(0,0,0),(20,20,20))
        self.line = cv2.erode(self.line,None,iterations=2)
        self.line = cv2.dilate(self.line,None,iterations=2)
        #CHANGE NONE
    
        #lineContours,_ = cv2.findContours(self.line, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(self.line) > 100:
            #largestContour = max(lineContours,key=cv2.contourArea)
            m = cv2.moments(self.line)
            if m['m00'] > 0:
                xPos = int(m['m10']/m['m00'])
                yPos = int(m['m01']/m['m00'])
                error = (xPos-(frameWidth/2))/679*100
                cv2.circle(roi,(xPos,yPos),5,(255,0,0),-1)
                cv2.circle(self.frame,(679,906),5,(0,255,0),-1)
                cv2.line(self.frame,(679,906),(xPos,yPos),(0,255,0),2)
                opposite = xPos-679
                adjacent = 906-yPos
                angleRad = math.atan2(opposite, adjacent)
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
    follower.follow(cap)