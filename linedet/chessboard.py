import cv2
import numpy as np
import os 
import utils as utils

from matplotlib import pyplot as plt
from matplotlib import colors

testimpath = 'linedet/checkerboard.png'
img = cv2.imread(testimpath, cv2.IMREAD_UNCHANGED)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#ranges for blue
light_blue = np.array([100, 150, 0], np.uint8)
dark_blue = np.array([140, 255, 255], np.uint8)


#isolate blue
mask = cv2.inRange(imgHSV, light_blue, dark_blue)

#and with original image to make cleaner
result = cv2.bitwise_and(img, img, mask=mask)

#convert to grayscale
resultGRAY = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

#convert to black and white
thresh, resultBW = cv2.threshold(resultGRAY, 50, 255, cv2.THRESH_BINARY)

#invert so background is white
resultBWinv = cv2.bitwise_not(resultBW)

# plt.subplot(1,2,1)
# plt.imshow(mask, cmap="gray")
# plt.subplot(1,2,2)
# plt.imshow(result)
# plt.show()


# cv2.imshow('hi', resultBWinv)
# cv2.waitKey(0)


#find chess board corners

#left
retright, cornersright = cv2.findChessboardCorners(resultBWinv, (4,3), None)

# img2 = cv2.drawChessboardCorners(img, (4,3), cornersright, retright)
# cv2.imshow('right', img2)
# cv2.waitKey(0)

#right
retleft, cornersleft = cv2.findChessboardCorners(resultBWinv, (5,4), None)


# img3 = cv2.drawChessboardCorners(img, (5,4), cornersleft, retleft)
# cv2.imshow('left', img3)
# cv2.waitKey(0)


'''find pixel distances and compare'''


#flip shape here for numpy 
utils.pixel_distances(cornersright, (3,4,-1))
utils.pixel_distances(cornersleft, (4,5,-1))

# for i in range(cornersleft.shape[0]-1):
#     point1 = cornersleft[i]
#     point2 = cornersleft[i+1]
#     dist = np.linalg.norm(point1 - point2)
#     print(point1, point2, dist)

