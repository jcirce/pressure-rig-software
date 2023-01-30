import cv2
import numpy as np
import os 

from matplotlib import pyplot as plt

#cropping done manually right now, not so great to be doing it this way 
def crop(img):
    cropimg = img[0:360, 80:965]
    return cropimg

testfold = 'data/D20K5_withgrid1/'
for path in os.listdir(testfold):

    testimpath = testfold+path
    print(testimpath)

    #crop and change colorspace
    img = crop(cv2.imread(testimpath, cv2.IMREAD_UNCHANGED))
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #apply thresholding
    ret, mask = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)

    #find contours
    contours, hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #find chess board corners
    retchess, corners = cv2.findChessboardCorners(mask, (6,4), None)

    #terminating criteria 
    # https://www.tutorialspoint.com/how-to-find-patterns-in-a-chessboard-using-opencv-python
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    if retchess == True:
        corners2 = cv2.cornerSubPix(mask, corners, (11,11), (-1,-1), criteria)
        cv2.imshow('img', mask)
        cv2.waitKey(0)
        #draw countours
        #img = cv2.drawContours(img, contours, -1, (0,255,0),3)
        img = cv2.drawChessboardCorners(mask, (6,4), corners, retchess)
        cv2.imshow('Contours and Chessboard', mask)
        cv2.waitKey(0)



    

    # images = [mask]

    # for i in range(2):
    #     plt.subplot(2, 2, i+1)
    #     plt.imshow(images[i])
    # plt.show()

    # try this next 
    # https://www.geeksforgeeks.org/find-and-draw-contours-using-opencv-python/
    # look into canny, sorel, fill area, thresholds for contours