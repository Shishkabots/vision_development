import numpy as np
import cv2 as cv
img = cv.imread('star.jpg',0)
ret,thresh = cv.threshold(img,127,255,0)
<<<<<<< HEAD
contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
M = cv.moments(cnt)
print(M)
if M["m00"] != 0:
 cx = int(M["m10"] / M["m00"])
 cy = int(M["m01"] / M["m00"])
 print("CX: ", cx)
 print("CY: ", cy)
else:
 cX, cY = 0, 0
=======
contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
cnt = contours[0]
M = cv.moments(cnt)
print(M)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print("CX: ", cx)
print("CY: ", cy)
>>>>>>> e6f1e9a5bf41c431d60754a21540325ff90a3600
