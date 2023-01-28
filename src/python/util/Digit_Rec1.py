from imutils.perspective import four_point_transform 
from imutils import contours 
import imutils 
import cv2 
from numpy import reshape
import numpy as np
#from Seg7 import Segments

DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
    (1, 0, 1, 0, 1, 0, 1): 0,
    (1, 0, 1, 0, 1, 1, 1): 0, #Experimental Key
    (1, 1, 1, 0, 1, 0, 1): 0,
    (0, 0, 1, 1, 1, 0, 1): 1,
	(0, 0, 1, 0, 0, 1, 0): 1,
    (0, 0, 1, 1, 0, 0, 1): 1, #Experimental Key 
    (0, 0, 1, 1, 1, 0, 0): 1, #Experimental
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 1, 0, 1): 8,
    (1, 0, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9,
    (1, 1, 1, 1, 0, 0, 1): 9,
    (1, 0, 1, 1, 1, 1, 0): 9,
    (0, 0, 0, 0, 0, 0, 0): -1 #error/unknown number  
}

def scale_up(img):
    scale_percent = 227 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized



#Note: imread loads only ONE image at a time right now
#Note 2: Could put this in a loop but need to figure out how to load multiple images just taken 
def get_digits(imag): 
    image = cv2.imread(imag)
    cv2.imshow("Image",image)
    cv2.waitKey(0)
    #image = imutils.resize(image, height = 500) #Resizes the Image
    image = scale_up(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50 ,200, 255)

    

    items = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(items)
    cnts = sorted(cnts, key = cv2.contourArea, reverse=True)
    dispaly = None 


    for c in cnts: 
            arc_Length = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c, 0.02 * arc_Length, True)
            if len(approx) == 4: 
                dispaly = approx
                break 

    #print(type(dispaly))
    
    warped = four_point_transform(gray,dispaly.reshape(4,2))
    output = four_point_transform(image,dispaly.reshape(4,2))
    # cv2.imshow("Output", output)
    # cv2.waitKey(0)

    '''
        lab = cv2.cvtColor(output, cv2.COLOR_BGR2LAB)
        l,a,b = cv2.split(lab)

        cv2.imshow("lab", lab)
        cv2.waitKey(0)

        kernel = np.ones((5,5), np.uint8)

        # threshold params
        low = 165
        high = 200
        iters = 3

        # make copy
        copy = b.copy()

        thresh = cv2.inRange(copy, low, high)

        # dilate
        for a in range(iters):
            thresh = cv2.dilate(thresh, kernel)

        # erode
        for a in range(iters):
            thresh = cv2.erode(thresh, kernel)

        # show image
        cv2.imshow("thresh", thresh)
        #cv2.imwrite("threshold.jpg", thresh)
        
    '''

    '''

    img2 = cv2.imread("opentest.png")
    output1 = four_point_transform(img2,dispaly.reshape(4,2))
    cv2.imshow("Image2", output1)
    cv2.waitKey(0)
    '''

    thresh = cv2.threshold(warped, 0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    #thresh = ~thresh

    iters = 4


    # cv2.imshow("thresh2", thresh)
    # cv2.waitKey(0)

    for a in range(iters):
        thresh = cv2.dilate(thresh, kernel)
        # cv2.imshow("k1", thresh)
        # cv2.waitKey(0)

    # erode
    for a in range(iters):
        thresh = cv2.erode(thresh, kernel)
        # cv2.imshow("k2", thresh)
        # cv2.waitKey(0)


    '''cv2.imwrite('savedImage.jpg', thresh)

    img = Image.open('savedImage.jpg')
    inv_img = ImageChops.invert(img)
    inv_img.show()'''


    #draws the contours around the number 
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(output, [contour], 0, (0,255,0), 3)

    #---------------------()----------------------#

    
    bounds = []
    h, w = image.shape[:2]
    #print(w)
    for contour in contours:
        left = w
        right = 0
        top = h
        bottom = 0
        for point in contour:
            point = point[0]
            x, y = point
            if x < left:
                left = x
            if x > right:
                right = x
            if y < top:
                top = y
            if y > bottom:
                bottom = y
        tl = [left, top]
        br = [right, bottom]
        bounds.append([tl, br])

    # crop out each number
    digits = []
    cuts = []
    number = 0
    for bound in bounds:
        tl, br = bound
        cut_img = thresh[tl[1]:br[1], tl[0]:br[0]]
        #can do a append if it is big enough 
        (Hei,Wid) = cut_img.shape
        #print(Hei,Wid) 
        if Wid >= 15 and (Hei>= 60):
            cuts.append(cut_img)
        number += 1
         
    
    for c in cuts:
        #roi = cuts[c]
        cv2.imshow("Num", c)
        cv2.waitKey(0)


    
        (roiH, roiW) = c.shape
        (h,w) = c.shape
        #print(roiH,roiW)
        #keep number 101 for one of these values in mind 
        (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
        #need to find width and height of cuts 


        dHC = int(roiH * 0.05)
        segments = [
		((0, 0), (w, dH)),	# top
		((0, 0), (dW, h // 2)),	# top-left
		((w - dW, 0), (w, h // 2)),	# top-right
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
		((0, h // 2), (dW, h)),	# bottom-left
		((w - dW, h // 2), (w, h)),	# bottom-right
		((0, h - dH), (w, h))	# bottom
        ]
        on = [0] * len(segments) # creates a list of 7
 
        

        
        for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
            segROI = c[yA:yB, xA:xB]
            total = cv2.countNonZero(segROI)
            area = (xB - xA) * (yB - yA)
            cv2.imshow("Num" + str(i), c)
            cv2.waitKey(0)
            
            
            
            #print(segROI)
            # print(total)
            #print(area)

            det = total / float(area)
            #print(det)


            if  det > 0.5:
                on[i]= 1
                
        
    
        digit = DIGITS_LOOKUP[tuple(on)]
        digits.append(digit)
        print(digit)
        Make_num = []
        Make_num.append(digit)

        for x in range(len(Make_num)):
            pass 





        



        # for i in digits:
        #     print(digits[i])
        
#sort so contours with bigger areas are at the front of the list 
# find cutoff so they won't get accepted 
        


#---------------------------------------------------------------------------------------------------------------------#
    '''
    model = Segments()
    index = 0
    
    for x in range(len(cuts)):
        # save image
        #cv2.imwrite(str(index) + "_" + str(number) + ".jpg", cut)

        # process
        model.digest(cuts[x])
        number = model.getNum() #THIS IS THING WE PASS TO OTHER PROGRAM 

        #showing values guessed by the system 
        print(number)
        cv2.imshow(str(index), cuts[x])
        cv2.waitKey(0)
    cv2.imshow("contours", output)
    cv2.waitKey(0)
    '''
    

def main():
    get_digits()

if __name__ == "__main__":
    main()

#0: Works 
#1: Works
#2: Works
#3: Works
#4: Works
#5: Works
#6: 
#7: Works
#8: 
#9: 




#Plan 
#Test out each indivisual number on the seven seg display. 
#Record W and H values 
#Record Dictionary Key values that are not idenitfy.
#Make camera straight 
#Chillling : ) 