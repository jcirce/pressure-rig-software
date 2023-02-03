import numpy as np
import cv2
from arduino_comms import CommsController
import os
from setup import Tube
from Digit_Rec1 import get_digits

c = CommsController() 
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("cannot open camera")
    exit()
f = open("psimap.txt", "a")

counter = 0 #test only runs for set pressure amount
photocounter = 0 

# #these values from jan/11 map
# bit = np.array([255, 200, 125,  90,  68,  55,  44,  35,  30,   25,   22,   18,   15,   14,   13,   12]) #16 commands 0-15 index
# psi = np.array([1.7, 2.0, 3.1, 4.0, 5.1, 6.0, 7.0, 8.2, 9.1, 10.1, 10.9, 12.1, 13.2, 13.6, 14.2, 14.6])

bit = np.linspace(0,100,101) #might cause error
kai = np.size(bit) - 1 #times want to take photos, twice number of bit commands we have

#up = True #tracking if pressure increasing or not

tube = Tube() #asks for name, number, test number
print(tube)

parent_dir = "/Users/student/desktop/pressure-rig-software/data/"
dir = str(tube) #makes sure its a string
path = os.path.join(parent_dir, dir)
os.mkdir(path) #makes dir for photos to go in
print("dir made for {}".format(dir))
print("path made for {}".format(path))

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
        print("sending {} bit".format(bit[counter]))
        c.append_command(b"R0%\n")
        s = f"S1,A{bit[counter]}%\n" 
        c.append_command(bytes(s, 'UTF-8'))
        a = c.responseList.get()
        #print("sent command {}".format(a))
        print("press m to take photo")

    if k == 109: #m pressed
        img_name = "{}.png".format(bit[counter])
        print("counter is {}".format(counter))
        print("\\")
        
        cv2.imwrite(os.path.join(path, img_name), frame)
        image = os.path.join(path, img_name).replace("\\", "/")
        print("{} written".format(image))
        psi, kpa = get_digits(image)
        f.write("{} , {} , {} \n".format(bit[counter], psi, kpa))
        
        counter += 1
        print("press spacebar to change pressure")
        #photocounter += 1

        # if counter == kai: #reached max index
        #     up = False
        #     print("now going backwards")
        

       # if up:
            #counter += 1 #increasing pressure
       # else:
           # counter -= 1 #decrease pressure
        
        # if counter == 0 and up == False:
        #     print("test done")
        #     break
        if counter == 255:
            print("DONE")
            break


    if k == 113:
        #press q to close camera
        break

    #f = open("psimap.txt")
    #f = write.()
    #f.close
f.close()
cap.release()
cv2.destroyAllWindows()
