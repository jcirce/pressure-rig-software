import cv2
import numpy as np
import os 
import curvaturetest
import random

from matplotlib import pyplot as plt

# choose the correct folder
testfold = 'bluelinephotos\s501_1/'
# iterates over all the files in a directory
for path in os.listdir(testfold): 
    testimpath = testfold+path
    print('Analyzing: ' + testimpath)

    split1 = testfold.split('\\')
    test = split1[1]
    print('Output Text File: ' + test)

    #crop and change colorspace
    img = cv2.imread(testimpath, cv2.IMREAD_UNCHANGED)
    
    height, width = img.shape[:2]
    # rotation:
    # angle = 0
    # rot_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    # rot_img = cv2.warpAffine(img, rot_matrix, (width, height))

    screen_x = 51.1175
    screen_y = 28.8925
    pxl_cm_x = width/screen_x
    pxl_cm_y = height/screen_y
    print(width)
    print(pxl_cm_x)

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converts cropped image to gray scale

    #apply thresholding
    ret, mask = cv2.threshold(img2, 55, 255, cv2.THRESH_BINARY)
    # threshold value: (-, thresh, -, cv2.THRESH_BINARY)
    # black marker on blue: 55
    # black marker on pink: 55
    # black marker on white: 80
    
    #find contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours --> (x,y) coords, list of contours found, each contour is a list of points
        # hierarchy --> info about which contours are inside/outside depends onn retrieval mode
        # contours are the boundaries of images
    
    # test plot
    mask2 = mask.copy()
    mask3 = cv2.drawContours(mask2, contours, -1, (0,255,0), 10)

    # This shows the steps of converting from original image to final
    # plt.subplot(2,2,1)
    # plt.imshow(img) 
    # plt.subplot(2,2,2)
    # plt.imshow(img2)
    # plt.subplot(2,2,3)
    # plt.imshow(mask)
    # plt.subplot(2,2,4)
    # plt.imshow(mask3)
    # plt.show()

    # This prints every photo in file in the converted version
    # plt.figure()
    # plt.imshow(mask)
    # plt.title(path)
    # plt.show()

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

    x = np.array(x, dtype=np.int64)
    y = np.array(y, dtype=np.int64)

    xy = [[xx, yy] for xx, yy in zip(x, y)]
    # print(min(xy))
    # print(max(xy))

    xy = np.array(xy, dtype=np.int64)
    sort_XY = np.argsort(xy[:, 0])
    xy = xy[sort_XY]
    #print(xy)

    # break up the contour line into three sets of x values
    length = len(xy)//3
    xy_1 = xy[0:length]
    xy_2 = xy[length:2*length]
    xy_3 = xy[2*length::]

    curvature = []

    # randomely pick 1 number per set to calculate curvature
    # repeat 100 times, and take average
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

    # record results in output text file (change the name to what you want the output file to have, and correct folder)
    with open("ani-text-file/curvature_data\s501_1.txt", 'a') as file:
        file.write("File: " + path + " Curvature: "+ str(curvature_avg) + "\n")
