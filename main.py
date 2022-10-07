import cv2
import numpy as np
import RPi.GPIO as gpio
import robotScripts.drive

img = cv2.imread("/home/admin/robocup_2023/straight.png")
cv2.imshow("Straight", img)
print("Window Shown")
cv2.waitKey()

robot = robotScripts.drive.driveBase(1, 2, 3, 4)

robot.drive(10, 2)