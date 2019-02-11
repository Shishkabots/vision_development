import cv2
import math 
import numpy as np

class Tup:
	def __init__(self, distance, slope, point1, point2):
		self.distance = distance
		self.slope = slope
		self.point1 = point1
		self.point2 = point2

im = cv2.imread("woodslab.jpg")

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);
gray = cv2.GaussianBlur(gray, (5, 5), 0)
bin = cv2.threshold(gray, 120, 255, 1) # inverted threshold (light obj on dark bg)
bin = cv2.dilate(bin, None)  # fill some holes
bin = cv2.dilate(bin, None)
bin = cv2.erode(bin, None)   # dilate made our shape larger, revert that
bin = cv2.erode(bin, None)
bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


# creates nCr(4, 2) = 6 lines (represented in the Tup class), sorts them by distance, and returns the third one (representing the long side of the rectangle)
# pairs of points (i.e. lines) are: (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)
def get_long_side(contours):
	rc = cv2.minAreaRect(contours[0])
	box = cv2.boxPoints(rc)

	tups = [] #list of tuples

	for (i, p1) in enumerate(box):
		for (j, p2) in enumerate(box):
			if i < j:
				ydiff = p2[1] - p1[1] # difference in y coords
				xdiff = p2[0] - p1[0] # difference in x coords
				distance = sqrt(xiff ** 2 + ydiff ** 2) # distance formula to find distance between 2 points
				slope = ydiff / (xdiff * 1.0)
				tups.append(Tup(distance, slope, p1, p2)) #add in the tuple into the list 

	tups.sort(key=distance)
	return tups[2]


'''
for p in box:
    pt = (p[0],p[1])
    print pt
    cv2.circle(im,pt,5,(200,0,0),2)
cv2.imshow("plank", im)
cv2.waitKey()
'''

