import cv2
import numpy as np
import os 
import curvaturetest
import random

from matplotlib import pyplot as plt

#cropping done manually right now, not so great to be doing it this way 
def crop(img):
    cropimg = img[0:900, 200:900]
    return cropimg

testfold = 'pressure-rig-software/bluelinephotos\s402_1/'  # folder with images
for path in os.listdir(testfold): # iterates over all the files in a directory
    testimpath = testfold+path
    print('Analyzing: ' + testimpath)

    split1 = testfold.split("/")
    split2 = split1[1].split('\\')
    test = split2[1] + ' curvature data'
    print('Output Text File: ' + test)

    #crop and change colorspace
    img = cv2.imread(testimpath, cv2.IMREAD_UNCHANGED)
    # img = crop(img)
    # angle = 0
    height, width = img.shape[:2]
    # rot_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    # rot_img = cv2.warpAffine(img, rot_matrix, (width, height))

    screen_x = 51.1175
    screen_y = 28.8925
    pxl_cm_x = width/screen_x
    pxl_cm_y = height/screen_y
    print(width)
    print(pxl_cm_x)
    # resize_img = rot_img.resize(n_width, n_height)

    #img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converts cropped image to gray scale
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #apply thresholding
    #ret, mask = cv2.threshold(img2, 180, 255, cv2.THRESH_BINARY)
    ret, mask = cv2.threshold(img2, 80, 255, cv2.THRESH_BINARY)
    # threshold of 30 is good for the black marker on blue, but needs experimenting
    # cuz it cuts out a lot of the data
    # threshold of 80 is good for the blue marker on white
    # threshold of 100 is good for multiple colors to break off the sections
    # but can't necessarily isolate different colors yet

        # ret = 127 (threshold value)
        # mask = the img2 converted to a binary

    #find contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours --> (x,y) coords, list of contours found, each contour is a list of points
        # hierarchy --> info about which contours are inside/outside depends onn retrieval mode
        # contours are the boundaries of images
    
    # test plot
    mask2 = mask.copy()
    mask3 = cv2.drawContours(mask2, contours, -1, (0,255,0), 10)

    # plt.subplot(2,2,1)
    # plt.imshow(img) 
    # plt.subplot(2,2,2)
    # plt.imshow(img2)
    # plt.subplot(2,2,3)
    # plt.imshow(mask)
    # plt.subplot(2,2,4)
    # plt.imshow(mask3)
    # plt.show()

    plt.figure()
    plt.imshow(mask)
    plt.show()

    x = []
    y = []
    xy = [[]]

    # Loop through the list of contours
    for contour in contours:
        # Extract x and y coordinates of contour points
        contour_X = [point[0][0] for point in contour]
        contour_Y = [point[0][1] for point in contour]

        # Append the coordinates to the respective lists
        x.extend(contour_X)
        y.extend(contour_Y)

    x = x[4::]
    y = y[4::]

    # print('min x: ' + str(min(x)))
    # print('max x: ' + str(max(x)))
    # print('min y: ' + str(min(y)))
    # print('max y: ' + str(max(y)))

    # print('length x: ' + str(len(x)))
    # print('length y: ' + str(len(y)))
    # print("Number of Contours found = " + str(len(contours)))

    # x_1 = [x[500], x[1000], x[1500], x[2000], x[2500], x[3000], x[3500]]
    # y_1 = [y[500], y[1000], y[1500], y[2000], y[2500], y[3000], y[3500]]

    # print(x_1)
    # print(y_1)
    x = np.array(x, dtype=np.int64)
    y = np.array(y, dtype=np.int64)

    xy = [[xx, yy] for xx, yy in zip(x, y)]
    # print(min(xy))
    # print(max(xy))


    xy = np.array(xy, dtype=np.int64)
    sort_XY = np.argsort(xy[:, 0])
    xy = xy[sort_XY]
    #print(xy)

    length = len(xy)//3

    xy_1 = xy[0:length]
    xy_2 = xy[length:2*length]
    xy_3 = xy[2*length::]

    curvature = []

    for i in range(0,100):
        one = random.randint(0, length-1)
        two = random.randint(0, length-1)
        three = random.randint(0, length-1)
        x = [xy_1[one][0], xy_2[two][0], xy_3[three][0]]
        y = [xy_1[one][1], xy_2[two][1], xy_3[three][1]]
        curve = curvaturetest.curvature(x,y, pxl_cm_x, pxl_cm_y)
        curvature.append(curve)

    curvature_avg = np.mean(curvature)
    # print(min(curvature))
    # print(max(curvature))
    # print(curvature_avg)

    with open(test, 'a') as file:
        file.write("File: " + path + " Curvature: "+ str(curvature_avg) + "\n")
