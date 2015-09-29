import cv2
import numpy as np

def getBoundingBoxes(filename):

    img = cv2.imread(filename);
    blur = cv2.blur(img,(11,11))
    (ret,thresh) = cv2.threshold(blur,40,255,cv2.THRESH_BINARY)
    (ret,blur) = cv2.threshold(blur,240,255,cv2.THRESH_BINARY)

    thr = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(thr,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    bbox = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        #area = cv2.contourArea(contour)
        #cv2.drawContours(img,[contours[0]],0, (0,255,0), 3)
        #cv2.rectangle(img,(x,y),(x+w,y+h),(100,255,100),2,8,0)
        bbox.append((x,y,x+w,y+h))
    return bbox

#print getBoundingBoxes('1.jpeg') 
#cv2.imwrite('1_bb.jpeg',img)
