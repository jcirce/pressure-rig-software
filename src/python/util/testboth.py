import numpy as np
import cv2
from arduino_comms import CommsController
from loadcell import LoadCell
import os
from setup import Tube

c = CommsController() 
cap = cv2.VideoCapture(0)
l = LoadCell()

if not cap.isOpened():
    print("cannot open camera")
    exit()

counter = 0 #test only runs for set pressure amount
photocounter = 0 

#these values from jan/11 map
bit = np.array([255,    88,   61,   41,   30,   22,   16,   12,   11,   10,     9,     6,     4,     2,     1,     0]) 
psi = np.array([1.7,   3.3,  4.4,  5.9,  7.2,  8.7, 10.3, 11.6, 12.0, 12.5,  13.0,  14.7,  16.0,  17.7,  18.8,  19.9])
kpa = np.array([11.0, 22.8, 30.3, 40.7, 49.6, 60.0, 71.0, 80.0, 82.7, 86.2,  89.6, 101.4, 110.3, 122.0, 129.6, 137.2])



kai = np.size(bit) - 1 #times want to take photos, twice number of bit commands we have, 15

up = True #tracking if pressure increasing or not

tube = Tube() #asks for name, number, test number
print(tube)

parent_dir = "/Users/student/desktop/pressure-rig-software/data-good"
dir = str(tube) #makes sure its a string
path = os.path.join(parent_dir, dir)
os.mkdir(path) #makes dir for photos to go in
print("dir made for {}".format(dir))
print("path")
print(path)

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
        #print("sending {} bit".format(bit[counter]))
        c.append_command(b"R0%\n")
        s = f"S1,A{bit[counter]}%\n" 
        c.append_command(bytes(s, 'UTF-8'))
        a = c.responseList.get()
        #print("sent command {}".format(a))
        print("press f to take force reading")
        # print("press m to take photo")

    if k == 102: #f pressed
        force = l.get_reading()
        print("force is = {}".format(force))
        print("press m to take photo")


    if k == 109: #m pressed
        img_name = "{}_{}_kPa{}.png".format(tube, photocounter, kpa[counter])
        cv2.imwrite(os.path.join(path, img_name), frame)
        print("{} written".format(img_name))
        print("press spacebar to change pressure")
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

    if k == 113:
        #press q to close camera
        break

cap.release()
cv2.destroyAllWindows()
