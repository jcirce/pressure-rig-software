import numpy as np
import cv2
from arduino_comms import CommsController
import os
from setup import Tube

c = CommsController() 
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("cannot open camera")
    exit()

counter = 0 #test only runs for set pressure amount

bit = np.array([255, 160, 113,  87,  69,  56,  47,  40,   34,   29,   25])
psi = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.1])
kai = np.size(bit) - 1 #times want to take photos

tube = Tube()
print(tube)

parent_dir = "/Users/student/desktop/pressure-rig-software/src/python/util"
dir = str(tube) #makes sure its a string
path = os.path.join(parent_dir, dir)
os.mkdir(path) #makes dir for photos to go in
print("dir made for {}".format(dir))

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

    if k == 32:
        #print("up pressure")
        print("sending {} bit".format(bit[counter]))

        c.append_command(b"R0%\n")
        s = f"S1,A{bit[counter]}%\n"
        c.append_command(bytes(s, 'UTF-8'))
        a = c.responseList.get()
        print("sent command {}".format(a))

    if k == 109:
        #print("take photo")
        img_name = "psi_{}.png".format(psi[counter])
        cv2.imwrite(os.path.join(path, img_name), frame)
        print("{} written".format(img_name))
        counter += 1

        if counter > kai:
                print("end of test")
                break

    if k == 113:
        break


cap.release()
cv2.destroyAllWindows()
exit()

