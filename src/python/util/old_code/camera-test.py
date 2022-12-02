import numpy as np
import cv2
from arduino_comms import CommsController
#import os
from setup import Tube

c = CommsController() 

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("cannot open camera")
    exit()

counter = 0 #test only runs for set pressure amount

bit = np.array([255, 160, 113,  87,  69,  56,  47,  40,   34,   29,   25])
psi = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.1])

def init(): 
    try:
        name = input("enter tube name (ex: D20K or S45M)")
        number = input("enter tube number")
        test = input("enter test number")

        tube = Tube(name, number, test)
        return tube
        
    except:
        print("error init")

tube = init() #set up tube name from CLI

parent_dir = "/Users/student/desktop/pressure-rig-software/src/python/util"
dir = str(tube) #makes sure its a string
#path = os.path.join(parent_dir, dir)
#os.mkdir(path) #makes dir for photos to go in
#print("dir made for {}".format(dir))
print("press space once camera focused")


while True:
    #capture frame by frame
    ret, frame = cap.read()

    #if frame read, ret is true
    if not ret:
        print("cant get frame")
        break

    cv2.imshow("test", frame)
    print("running before")

    k = cv2.waitKey(1000) 
    print("running after")

    if k%256 == 27:
        #escape pressed
        print("escape pressed... closing")
        break

    elif k%256 == 32: 
        #space pressed
        print("sending {} bit".format(bit[counter]))

        c.append_command(b"R0%\n")
        s = f"S1,A{bit[counter]}%\n"
        c.append_command(bytes(s, 'UTF-8')) 
        #see what its sending to arduino
        a=c.responseList.get()
        print("command is {}".format(a)) 
        #takes a few secs to for pressure to settle to steady state, 
        # also make sure camera in focus
        print("press 'm' to take photo")

    elif k%256 == ord('m'):
            #m pressed
            img_name = "psi_{}.png".format(psi[counter])
            
            cv2.imwrite(img_name, frame)
            print("{} written".format(img_name))
            print("press space to increase pressure")
            counter += 1

            if counter > 10:
                print("test done")
                break
    

#when done, release capture
cap.release()
cv2.destroyAllWindows()



