'''
Currently outstanding questions: should we be converting the image to gray in 1.1 (this will affect the pipeline).
If we are, we need to modify the pipeline as well. Also under consideration is whether it is easier to find contours when grayscale image is taken (equivalent
to asking whether we will have a more clear split of tape and non-tape under grayscale rather than RGB; I would imagine the answer is no, since tape is white)
Also, should we crop the image? Cropping image non-identically will mess with the distance from center of the camera to center of the tape. Ideally, 
we do not crop, unless leaving the black undistortion regions will cause problems in the GRIP pipeline.
'''

# TODO:
# Put in values for constants, also figure out loading in values for mapx and mapy
# Test/improve contour detection under different lightings
# Fix vertical box being returned for points (magic fix, possibly after input image was rescaled to 1280*720)
# Address resize issue (it's fine, just needed to rescale pixel value from 320*240 space to 1280*720 space)

import numpy as np
import cv2
import glob
import math
from enum import Enum

################################# 1.1: GET UNDISTORTION MAPPINGS #############################
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

training_images = glob.glob('undistortion_dataset/*.jpg')

for fname in training_images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(7,7),(-1,-1),criteria)
        imgpoints.append(corners)

# Function for calibrating the camera- returns camera matrix, distortion coeffs, rot/trans vectors
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
h, w = gray.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# get undistort matrices/mappings
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)

mapx_file = open('mapx_values.npy', 'w')
mapy_file = open('mapy_values.npy', 'w')
np.savetxt(mapx_file, mapx, delimiter=",", fmt='%.4f')
np.savetxt(mapy_file, mapy, delimiter=",", fmt='%.4f')

########################################### 1.2: UNDISTORT AND CROP EACH IMAGE ############################################

def undistort(img, mapx, mapy):
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #NOT IN GRAYSCALE ANYMORE
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR) # note that remap is forced 1080 x 720 input

    return dst # dst is the undistorted version of img

# crop the image
#x,y,w,h = roi
#dst = dst[y:y+h, x:x+w]

######################################### 2.1: FIND CENTER OF IMAGE #####################################################
class GripPipelinepython:
    """
    An OpenCV pipeline generated by GRIP.
    """
    
    def __init__(self):
        """initializes all values to presets or None if need to be set
        """

        self.__resize_image_width = 320.0
        self.__resize_image_height = 240.0
        self.__resize_image_interpolation = cv2.INTER_CUBIC

        self.resize_image_output = None

        self.__hsv_threshold_input = self.resize_image_output
        self.__hsv_threshold_hue = [0.0, 107.30375036037825]
        self.__hsv_threshold_saturation = [0.0, 79.48806844066841]
        self.__hsv_threshold_value = [131.47482050837374, 255.0]

        self.hsv_threshold_output = None

        self.__cv_dilate_src = self.hsv_threshold_output
        self.__cv_dilate_kernel = None
        self.__cv_dilate_anchor = (-1, -1)
        self.__cv_dilate_iterations = 3.0
        self.__cv_dilate_bordertype = cv2.BORDER_CONSTANT
        self.__cv_dilate_bordervalue = (-1)

        self.cv_dilate_output = None

        self.__cv_erode_src = self.cv_dilate_output
        self.__cv_erode_kernel = None
        self.__cv_erode_anchor = (-1, -1)
        self.__cv_erode_iterations = 3.0
        self.__cv_erode_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_bordervalue = (-1)

        self.cv_erode_output = None

        self.__find_contours_input = self.cv_erode_output
        self.__find_contours_external_only = False

        self.find_contours_output = None

        self.__filter_contours_contours = self.find_contours_output
        self.__filter_contours_min_area = 0.0
        self.__filter_contours_min_perimeter = 0.0
        self.__filter_contours_min_width = 20.0
        self.__filter_contours_max_width = 1000.0
        self.__filter_contours_min_height = 40.0
        self.__filter_contours_max_height = 1000.0
        self.__filter_contours_solidity = [0, 100]
        self.__filter_contours_max_vertices = 1000000.0
        self.__filter_contours_min_vertices = 0.0
        self.__filter_contours_min_ratio = 0.0
        self.__filter_contours_max_ratio = 1000.0

        self.filter_contours_output = None


    def process(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step Resize_Image0:
        self.__resize_image_input = source0
        (self.resize_image_output) = self.__resize_image(self.__resize_image_input, self.__resize_image_width, self.__resize_image_height, self.__resize_image_interpolation)

        # Step HSV_Threshold0:
        self.__hsv_threshold_input = self.resize_image_output
        (self.hsv_threshold_output) = self.__hsv_threshold(self.__hsv_threshold_input, self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)

        # Step CV_dilate0:
        self.__cv_dilate_src = self.hsv_threshold_output
        (self.cv_dilate_output) = self.__cv_dilate(self.__cv_dilate_src, self.__cv_dilate_kernel, self.__cv_dilate_anchor, self.__cv_dilate_iterations, self.__cv_dilate_bordertype, self.__cv_dilate_bordervalue)

        # Step CV_erode0:
        self.__cv_erode_src = self.cv_dilate_output
        (self.cv_erode_output) = self.__cv_erode(self.__cv_erode_src, self.__cv_erode_kernel, self.__cv_erode_anchor, self.__cv_erode_iterations, self.__cv_erode_bordertype, self.__cv_erode_bordervalue)

        # Step Find_Contours0:
        self.__find_contours_input = self.cv_erode_output
        (self.find_contours_output) = self.__find_contours(self.__find_contours_input, self.__find_contours_external_only)

        # Step Filter_Contours0:
        self.__filter_contours_contours = self.find_contours_output
        (self.filter_contours_output) = self.__filter_contours(self.__filter_contours_contours, self.__filter_contours_min_area, self.__filter_contours_min_perimeter, self.__filter_contours_min_width, self.__filter_contours_max_width, self.__filter_contours_min_height, self.__filter_contours_max_height, self.__filter_contours_solidity, self.__filter_contours_max_vertices, self.__filter_contours_min_vertices, self.__filter_contours_min_ratio, self.__filter_contours_max_ratio)


    @staticmethod
    def __resize_image(input, width, height, interpolation):
        """Scales and image to an exact size.
        Args:
            input: A numpy.ndarray.
            Width: The desired width in pixels.
            Height: The desired height in pixels.
            interpolation: Opencv enum for the type fo interpolation.
        Returns:
            A numpy.ndarray of the new size.
        """
        return cv2.resize(input, ((int)(width), (int)(height)), 0, 0, interpolation)

    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

    @staticmethod
    def __cv_dilate(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of higher value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for dilation. A numpy.ndarray.
           iterations: the number of times to dilate.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after dilation.
        """
        return cv2.dilate(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    @staticmethod
    def __cv_erode(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of lower value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for erosion. A numpy.ndarray.
           iterations: the number of times to erode.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after erosion.
        """
        return cv2.erode(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    @staticmethod
    def __find_contours(input, external_only):
        """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
        Args:
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Return:
            A list of numpy.ndarray where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        contours, hierarchy =cv2.findContours(input, mode=mode, method=method)
        return contours

    @staticmethod
    def __filter_contours(input_contours, min_area, min_perimeter, min_width, max_width,
                        min_height, max_height, solidity, max_vertex_count, min_vertex_count,
                        min_ratio, max_ratio):
        """Filters out contours that do not meet certain criteria.
        Args:
            input_contours: Contours as a list of numpy.ndarray.
            min_area: The minimum area of a contour that will be kept.
            min_perimeter: The minimum perimeter of a contour that will be kept.
            min_width: Minimum width of a contour.
            max_width: MaxWidth maximum width.
            min_height: Minimum height.
            max_height: Maximimum height.
            solidity: The minimum and maximum solidity of a contour.
            min_vertex_count: Minimum vertex Count of the contours.
            max_vertex_count: Maximum vertex Count.
            min_ratio: Minimum ratio of width to height.
            max_ratio: Maximum ratio of width to height.
        Returns:
            Contours as a list of numpy.ndarray.
        """
        output = []
        for contour in input_contours:
            x,y,w,h = cv2.boundingRect(contour)
            if (w < min_width or w > max_width):
                continue
            if (h < min_height or h > max_height):
                continue
            area = cv2.contourArea(contour)
            if (area < min_area):
                continue
            if (cv2.arcLength(contour, True) < min_perimeter):
                continue
            hull = cv2.convexHull(contour)
            solid = 100 * area / cv2.contourArea(hull)
            if (solid < solidity[0] or solid > solidity[1]):
                continue
            if (len(contour) < min_vertex_count or len(contour) > max_vertex_count):
                continue
            ratio = (float)(w) / h
            if (ratio < min_ratio or ratio > max_ratio):
                continue
            output.append(contour)
        return output

def find_center(img):
    pipeline = GripPipelinepython()
    pipeline.process(img)
    # x, y, w, h = cv2.boundingRect(pipeline.filter_contours_output[0]) # not sure whether grabbing the first from the list works (do you not need the whole thing?)
    # cx = x + w/2
    # cy = y + h/2

    moments = cv2.moments(pipeline.filter_contours_output[0])
    cx = int(moments['m10']/moments['m00'])
    cy = int(moments['m01']/moments['m00'])

    return cx, cy

########################################## 2.2: SCALE PIXEL TO REAL DISTANCE #####################################################

def convert_dist(pixel_dist, height):
    return 0.0001 * (9.081 * height * pixel_dist)


########################################## 2.3a: IDENTIFYING THE PROPER SIDE OF THE TAPE (LONG SIDE) #########################################
class Tup:
    def __init__(self, distance, slope, point1, point2):
        self.distance = distance
        self.slope = slope
        self.point1 = point1
        self.point2 = point2

# returns slope of line
def find_longer_line(img):
    pipeline = GripPipelinepython()
    pipeline.process(img)
    contours = pipeline.filter_contours_output

    # returns m, y0, and x0 of longer line
    rc = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(rc)
    box = np.int0(box)

    tups = [] #list of tuples

    # print("type of variable rc:", type(rc))
    # print("type of variable box:", type(box))
    # print("minAreaRect elements, i.e. from variable rc: ")
    # print("center_x and center_y:", rc[0])
    # print("width and height:", rc[1])
    # print("angle:", rc[2])
    # print("boxPoints elements, i.e. from variable box: ")
    # for p in box:
    #     print(p[0], p[1])


    # resizing img from 1280x720 to 320, 240
    img = cv2.resize(img, (320, 240))
    # print(img.shape)
    # print(len(box))
    # print("number of contours:", len(contours))d
    # cv2.drawContours(img, contours[0], -1, (0, 0, 255), 2)
    # cv2.imshow("draw contours", img)
    # cv2.waitKey(0)

    cv2.drawContours(img, [box], -1, (0, 0, 255), 2)
    cv2.imshow("draw contours", img)
    cv2.waitKey(0)

    for (i, p1) in enumerate(box):
        for (j, p2) in enumerate(box):
            if i < j:
                ydiff = p2[1] - p1[1] # difference in y coords
                xdiff = p2[0] - p1[0] # difference in x coords

                distance = math.sqrt(xdiff ** 2 + ydiff ** 2) # distance formula to find distance between 2 points
                if(xdiff == 0) :
                      slope = 10000000000
                else :
                      slope = ydiff/(xdiff * 1.0)
                # print(ydiff)
                # print(xdiff)
                tups.append(Tup(distance, slope, p1, p2)) #add in the tuple into the list 

    tups.sort(key=lambda tup: tup.distance)
    return tups[2].slope


########################################## 2.3b: ANGLE FROM TAPE SIDE TO CAMERA FACING #####################################################

def get_cameraToTape_Theta(m):
    # y = y0 + m(x - x0)
    # using one point x = x0, another point x = x0 + 100
    # find two points on the line. camera forward defines the y of the image, so finding the angle from the camera line is the same as finding the
    # angle from just the y axis. After two points on the line are found, find delta y and delta x, and then get atan.

    # actually, only the slope is needed (angle is found with atan(slope), since the original argument (y2 - y1) / (x2 - x1) is equivalent to slope anyway)

    # x1 = x0 + 100 # hundred pixels rightward (can be any value, since ratio remains the same as long as x1 - x0 isn't too small)
    # y1 = y0 + m*(x1 - x0) # corresponding y change for the x change

    theta = math.atan(m)
    return theta

########################################## 2.4: FINAL R AND THETA CALCULATION #####################################################

# from robot center to (potentially offset) target point on tape strip
# NOTE THAT THE PIXEL DELTA_X AND DELTA_Y CALCULATIONS ARE RELIANT ON THE ORIGINAL DIMENSIONS OF THE IMAGE BEING PRESERVED (if this constraint
# needs to be lifted, we need to write a bit of code for accounting for scaling)
def get_final_R_theta(img, robot_offset_x, robot_offset_y, tape_offset_x, tape_offset_y, height):
    tape_offset_r = math.sqrt(tape_offset_x ** 2 + tape_offset_y ** 2)
    # convention throughout is that negative theta is clockwise, so if x is negative, theta is negative
    tape_offset_theta = math.copysign(math.pi / 2, tape_offset_x) if tape_offset_y == 0 else math.atan(tape_offset_x / tape_offset_y) # IT'S X/Y SINCE THETA IS BEING MEASURED FROM Y AXIS

    pixel_x, pixel_y = find_center(img) # note that the find_center returns things as 320x240 (width x height) images. Need to rescale back to 1280x720
    print(" init return x: ", pixel_x)
    print(" init return y: ", pixel_y)
    pixel_x *= 1280.0/320.0
    pixel_y *= 720.0/240.0

    print(" init return x: ", pixel_x)
    print(" init return y: ", pixel_y)

    pixel_delta_x = img.shape[1] / 2 - pixel_x
    print( "img x", img.shape[1]/2)
    print (" pixel delta x:", pixel_delta_x)
    pixel_delta_y = img.shape[0] / 2 - pixel_y
    print( "img y", img.shape[0]/2)
    print (" pixel delta y:", pixel_delta_y)
    camera_r = convert_dist(math.sqrt(pixel_delta_x ** 2 + pixel_delta_y ** 2), height)
    # again, intentional x/y (see the image, it's weird)
    camera_theta = math.copysign(math.pi / 2, pixel_delta_x) if pixel_delta_y == 0 else math.atan(pixel_delta_x/pixel_delta_y)    # for negative pixel_delta_x, should take return a negative angle (i.e. clockwise is neg. theta)

    # just realized that the namings are weird, just swapped them around to be from the perspective of the camera (but new namings are also
    # weird, since y is cos and x is sin)
    camera_delta_y = camera_r * math.cos(camera_theta)
    camera_delta_x = camera_r * math.sin(camera_theta)

    cameraToTape_theta = get_cameraToTape_Theta(find_longer_line(img))

    tape_delta_x = tape_offset_r * math.cos(cameraToTape_theta + tape_offset_theta)
    tape_delta_y = tape_offset_r * math.sin(cameraToTape_theta + tape_offset_theta)

    delta_y = robot_offset_y + camera_delta_y + tape_delta_y
    delta_x = robot_offset_x + camera_delta_x + tape_delta_x
    r = math.sqrt(delta_y ** 2 + delta_x ** 2)
    theta = math.copysign(math.pi / 2, delta_x) if delta_y == 0 else math.atan(delta_x/delta_y) # yes, it is delta_x/delta_y

    return r, theta

# (3 is same as 2.3)


############################################################################################################################
'''
# full pipeline
img = cv2.imread("live_image")
mapx, mapy = LOAD_FROM_FILE # need to find the way to load from file properly (was not working before)
robot_offset_x, robot_offset_y = 0
tape_offset_x, tape_offset_y = 0
height = VALUE_3 # in inches
# find r, theta for moving to correct point
img = undistort(img, mapx, mapy)
r, theta = get_final_R_theta(img, robot_offset_x, robot_offset_y, tape_offset_x, tape_offset_y, height) # theta positive is clockwise turn, theta negative is counterclockwise turn
# find theta to align to the tape direction
img = cv2.imread("new_image_after_movement")
turn_theta = get_Tape_Theta(find_longer_line(img))
'''

####################################################################################################################

# for testing
#img = cv2.imread("four_sides.png")
img = cv2.imread("height_13.5_radius_2.5to3.5.jpg")
# mapx and mapy already there
robot_offset_x, robot_offset_y = 0, 0
tape_offset_x, tape_offset_y = 0, 0
height = 13.5

img = undistort(img, mapx, mapy)
# print("image size is ", img.shape)
r, theta = get_final_R_theta(img, robot_offset_x, robot_offset_y, tape_offset_x, tape_offset_y, height)
print("radius:", r)
print("angle in degrees:", theta * 180 / math.pi)
