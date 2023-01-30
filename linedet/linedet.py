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

    img = crop(cv2.imread(testimpath, cv2.IMREAD_UNCHANGED))
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    ret, mask = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)

    contours, hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0,255,0),3)
    cv2.imshow('Contours', img)
    cv2.waitKey(0)
    

    # images = [mask]

    # for i in range(2):
    #     plt.subplot(2, 2, i+1)
    #     plt.imshow(images[i])
    # plt.show()

    # try this next 
    # https://www.geeksforgeeks.org/find-and-draw-contours-using-opencv-python/
    # look into canny, sorel, fill area, thresholds for contours