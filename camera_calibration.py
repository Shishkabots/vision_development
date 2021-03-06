# DO NOT RUN THIS CODE ON IMAGES OTHER THAN CHESSBOARDS (the images will be deleted, but now they won't be)

import numpy as np
import cv2
import glob
import os

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(7,7),(-1,-1),criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        #cv2.drawChessboardCorners(img, (7,7), corners,ret)
        #cv2.imshow('img',img)
        #cv2.waitKey(500)
    #else:
        #os.remove(fname)
        #print "removed file", fname

cv2.destroyAllWindows()
print len(images)


# Function for calibrating the camera- returns camera matrix, distortion coeffs, rot/trans vectors
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
h, w = gray.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)

print mapx

mapx_file = open("mapx_values.npy", "w")
mapy_file = open("mapy_values.npy", "w")
np.save(mapx_file, mapx)
np.save(mapy_file, mapy)

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    dst = cv2.remap(gray,mapx,mapy,cv2.INTER_LINEAR) # changed image to gray,...

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite(fname[:-4] + '_calibrated.png', dst)

# Fix the issue
tot_error = 0
for i in xrange(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    tot_error += error

print "mean error: ", tot_error/len(objpoints)