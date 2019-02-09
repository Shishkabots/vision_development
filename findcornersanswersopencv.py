import cv2
import math 
import numpy as np

#NEW CODE
class Tup:
	def __init__(self, distance, slope, point1, point2):
		self.distance = distance
		self.slope = slope
		self.point1 = point1;
		self.point2 = point2; 
#NEW CODE ENDS

im = cv2.imread("woodslab.jpg")

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);
gray = cv2.GaussianBlur(gray, (5, 5), 0)
bin = cv2.threshold(gray,120,255,1) # inverted threshold (light obj on dark bg)
bin = cv2.dilate(bin, None)  # fill some holes
bin = cv2.dilate(bin, None)
bin = cv2.erode(bin, None)   # dilate made our shape larger, revert that
bin = cv2.erode(bin, None)
bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

rc = cv2.minAreaRect(contours[0])
box = cv2.boxPoints(rc)

#NEW CODE STARTS
tups = [] #list of tuples (each tuple consists of 2 points)
'''
4 3
4 2
4 1
3 2
3 1
2 1
'''

int count = 0;
int count2 = 0;
for i in box:
	for p in box:
		if (count2>count){
			pt = (p[0],p[1]) #first corner
			it = (i[0],i[1]) #second corner
			ydiff = (i[1]-p[1]) #difference in y coords
			xdiff = (i[0]-p[0]) #difference in x coords
			distance = math.sqrt((xiff)*(xdiff)+(ydiff)*(ydiff)) #distance formula to find distance between 2 points
			slope = ydiff/xdiff
			tups.append(Tup(distance, slope, pt, it)) #add in the tuple into the list 
		count2 += 1;
	count += 1;
	count2 = 0;
tups.sort(key=distance)
int count = 1;
for Tup in tups #find the tuple with the 5th largest distance
	if (count == 5)
		print Tup.distance; 
	count += 1
#NEW CODE FINISHES HERE

cv2.waitKey()


'''
for p in box:
    pt = (p[0],p[1])
    print pt
    cv2.circle(im,pt,5,(200,0,0),2)
cv2.imshow("plank", im)
cv2.waitKey()
'''


