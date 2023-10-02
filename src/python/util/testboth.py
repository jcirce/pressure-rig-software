import numpy as np
import cv2
from arduino_comms import CommsController
#from loadcell import LoadCell
import os
from setup import Tube

c = CommsController() 
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # for resolution

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # for resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # for resolution

#l = LoadCell()

if not cap.isOpened():
    print("cannot open camera")
    exit()

counter = 0 #test only runs for set pressure amount
photocounter = 0 

# #these values from isaiah's map 0-20psi
# bit = np.array([255,    88,   61,   41,   30,   22,   20,   18,   16,   14,   12,   11,   10,     9,     6,     4,     2,     1, 0]) 
# psi = np.array([1.7,   3.3,  4.4,  5.9,  7.2,  8.7,  9.2,  9.7, 10.3, 10.9, 11.6, 12.0, 12.5,  13.0,  14.7,  16.0,  17.7,  18.8, 19.9])
# kpa = np.array([11.0, 22.8, 30.3, 40.7, 49.6, 60.0, 63.4, 66.9, 71.0, 75.1, 80.0, 82.7, 86.2,  89.6, 101.4, 110.3, 122.0, 129.6, 137.2])

#0-30 reg limits
# bit = np.array([ 255,  120,  100,   70,   50,   40,   30,   25,   20,    13,    10,     7,     5,     4,     3,     2,     1, 0])
# psi = np.array([ 2.0,  3.8,  4.5,  6.0,  7.7,  9.0, 10.9, 12.2, 13.7,  16.9,  18.8,  21.0,  23.0,  24.1,  25.2,  26.6,  28.1, 29.7 ])
# kpa = np.array([13.8, 26.2, 31.0, 41.4, 53.1, 62.1, 75.2, 84.1, 94.5, 116.5, 129.6, 144.8, 158.6, 166.2, 173.7, 183.4, 193.7, 204.8 ])

#0-37 reg limits
# bit = np.array([255,   150,   60,   35,    25,    20,    15,    12,    10,     8,     6,     5,     4,     3,     2,     1, 0])
# psi = np.array([2.4,   3.9,  8.3, 12.2,  15.0,  17.1,  19.7,  21.7,  23.2,  25.1,  27.2,  28.4,  29.9,  31.3,  33.0,  34.8,  36.9])
# kpa = np.array([16.5, 26.9, 57.2, 84.1, 103.4, 117.9, 135.8, 149.6, 160.0, 173.1, 187.5, 195.8, 206.1, 215.8, 227.5, 239.9, 254.4])

#new sept 2023
bit = np.array([0,   102, 204, 306, 408, 510, 612, 714, 816, 918, 1020, 1122, 1224, 1326, 1428, 1530, 1632, 1734, 1836, 1938, 2040, 2142, 2244, 2346])#, 2448, 2550, 2652, 2754])#, 2856, 2958, 3060, 3162, 3264, 3366, 3468, 3570])
psi = np.array([0.1, 1.1, 2.2, 3.1, 4.1, 5.1, 6.2, 7.2, 8.2, 9.2, 10.2, 11.2, 12.2, 13.3, 14.2, 15.3, 16.3, 17.3, 18.3, 19.3, 20.3, 21.3, 22.3, 23.3])#, 24.4, 25.4, 26.4, 27.4, 28.4, 29.4, 30.5, 31.5, 32.5, 33.5, 34.5, 35.5])


kai = np.size(bit) - 1 #times want to take photos, twice number of bit commands we have,

up = True #tracking if pressure increasing or not

tube = Tube() #asks for name, number, test number
print(tube)

parent_dir = "/Users/student/desktop/pressure-rig-software/curvature-data-sept"
dir = str(tube) #makes sure its a string
path = os.path.join(parent_dir, dir)
os.mkdir(path) #makes dir for photos to go in 
print("dir made for {}".format(dir))

# print("path") 
# print(path)

#f = open("force_{}.txt".format(tube), "a")
#f.write("does this work")

print("press spacebar to start") #sends 255 bit

while True:
    #capture frame by frame
    ret, frame = cap.read()

    #if frame read, ret is true
    if not ret:
        print("cant get frame")
        break    

    cv2.imshow("test", frame)
    k = cv2.waitKey(1)
    #print(k) #prints int of key pressed

    if k == 32: #space pressed
        # print("sending {} psi".format(psi[counter]))
        # c.append_command(b"R0%\n")
        # s = f"S1,A{bit[counter]}%\n" 
        # c.append_command(bytes(s, 'UTF-8'))
        # a = c.responseList.get()
        print("input command should be {}, pressure should be {}".format(bit[counter], psi[counter]))
        #print("sent command {}".format(a))
        #print("press f to take force reading")
        print("press m to take photo")


    if k == "111": #o pressed
        counter = kai
        up = False
        print("now going backwards")



    if k == 109: #m pressed
        img_name = "{}_{}_PSI{}.png".format(tube, photocounter, psi[counter])
        cv2.imwrite(os.path.join(path, img_name), frame)
        print("{} written".format(img_name))
        
        photocounter += 1

        if counter == kai: #reached max index
            up = False
            print("now going backwards")

        if up:
            counter += 1 #increasing pressure
        else:
            counter -= 1 #decrease pressure
        
        if counter == 0 and up == False:
            print("test done")
            break

        # print("press o for no pressure")
        print("press spacebar to move on")

    # if k == 111: #o pressed
    #     print("sending no kpa")
    #     c.append_command(b"R0%\n")
    #     s = f"S1,A{bit[0]}%\n" 
    #     c.append_command(bytes(s, 'UTF-8'))
    #     a = c.responseList.get()
        
    #     print("press spacebar to change pressure")



    if k == 113:
        #press q to close camera
        break

#f.close()
cap.release()
cv2.destroyAllWindows()
