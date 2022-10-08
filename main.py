import cv2
import numpy as np
import RPi.GPIO as gpio
import robotScripts.drive
from time import sleep

#img = cv2.imread("/home/admin/robocup_2023/straight.png")
#cv2.imshow("Straight", img)
#print("Window Shown")
#cv2.waitKey()

robot = robotScripts.drive.driveBase(7, 11, 13, 15)

robot.drive(10)
print("driving")
sleep(10)
robot.stop()
print("stopped")