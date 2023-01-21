#https://stackoverflow.com/questions/64085745/get-the-contour-outline-from-a-png-image-with-the-correct-edges

import cv2
import numpy as np
from matplotlib import pyplot as plt

testfold = '../data/D20K5_1'
testimpath = '../data/D20K5_1/D20K5_1_psi_1.7.png'

#crop
def crop(img):
    cropimg = img[0:280, 0:360]
    return cropimg

img = crop(cv2.imread(testimpath, cv2.IMREAD_UNCHANGED))
img_grey = crop(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))


ret, mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
mask2 = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
    cv2.THRESH_BINARY, 11, 2)

contours, hierachy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (0,255,0),3)
cv2.imshow('Contours', img)
cv2.waitKey(0)

images = [mask, mask2]

# for i in range(2):
#     plt.subplot(2, 2, i+1)
#     plt.imshow(images[i])
# plt.show()

#try this next 
#https://www.geeksforgeeks.org/find-and-draw-contours-using-opencv-python/
#look into canny, sorel, fill area, thresholds for contours