import numpy as np
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("cannot open camera")
    exit()

while True:
    #capture frame by frame
    ret, frame = cap.read()

    #if frame read, ret is true
    if not ret:
        print("cant get frame")
        break
    cv2.imshow("test", frame)

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame', gray)
    #grey_img = cv2.imwrite()

    k = cv2.waitKey(1) 

    if k%256 == 32: 
        #space pressed
        img_name = "test_photo.png"
        cv2.imwrite(img_name, frame)
        print("{} written".format(img_name))
    

#when done, release capture
cap.release()
cv2.destroyAllWindows()


