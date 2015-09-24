import cv2
import numpy as np

img = cv2.imread('3.jpeg');
plt.imshow(img)
blur = cv2.blur(img,(8,8))
(ret,thresh) = cv2.threshold(blur,40,255,cv2.THRESH_BINARY)
(ret,blur) = cv2.threshold(blur,240,255,cv2.THRESH_BINARY)

thr = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(thr,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    #cv2.drawContours(img,[contours[0]],0, (0,255,0), 3)
    cv2.rectangle(img,(x,y),(x+w,y+h),(100,255,100),2,8,0)
