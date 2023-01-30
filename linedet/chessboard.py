import cv2
import numpy as np
import os 

from matplotlib import pyplot as plt
from matplotlib import colors

testimpath = 'linedet/checkerboard.png'
img = cv2.imread(testimpath, cv2.IMREAD_UNCHANGED)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

light_blue = np.array([100, 150, 0], np.uint8)
dark_blue = np.array([140, 255, 255], np.uint8)

mask = cv2.inRange(imgHSV, light_blue, dark_blue)
result = cv2.bitwise_and(img, img, mask=mask)


resultGRAY = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
thresh, resultBW = cv2.threshold(resultGRAY, 50, 255, cv2.THRESH_BINARY)
resultBWinv = cv2.bitwise_not(resultBW)

plt.subplot(1,2,1)
plt.imshow(mask, cmap="gray")
plt.subplot(1,2,2)
plt.imshow(result)
plt.show()


cv2.imshow('hi', resultBWinv)
cv2.waitKey(0)




#find chess board corners
retleft, cornersleft = cv2.findChessboardCorners(resultBWinv, (4,3), None)

print(retleft)

img2 = cv2.drawChessboardCorners(img, (4,3), cornersleft, retleft)
cv2.imshow('Contours and Chessboard', img2)
cv2.waitKey(0)



# #apply thresholding
# ret, mask = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY)



# retright, cornersright = cv2.findChessboardCorners(mask, (4,3), None)

# #terminating criteria 
# # https://www.tutorialspoint.com/how-to-find-patterns-in-a-chessboard-using-opencv-python
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# cv2.imshow('mask', mask)
# cv2.waitKey(0)

# if retleft == True:
#     #corners2 = cv2.cornerSubPix(mask, corners, (11,11), (-1,-1), criteria)

#     #draw chessboard corners
#     img = cv2.drawChessboardCorners(img2, (5,4), cornersleft, retleft)
#     cv2.imshow('Contours and Chessboard', img2)
#     cv2.waitKey(0)

