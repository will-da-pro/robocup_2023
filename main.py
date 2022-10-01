import cv2
import numpy as np

#img = cv2.imread('./tiles/JPEG/7. Dead End.jpg', cv2.IMREAD_UNCHANGED)
img = cv2.imread('./tiles/JPEG/1. Straight.jpg', cv2.IMREAD_UNCHANGED)
#img = np.full((1000,1000,3), 12, np.uint8)
#convert img to grey
#if img
try:    
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
except:
    print("error")
    img_grey = cv2.cvtColor(img, cv2.COLOR_GRAY)
#set a thresh
thresh = 1500
#get threshold image
ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#create an empty image for contours
img_contours = np.zeros(img.shape)
# draw the contours on the empty image
cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
#save image
cv2.imshow('Contours',img_contours) 
cv2.imshow('Grey', img_grey)
cv2.waitKey()