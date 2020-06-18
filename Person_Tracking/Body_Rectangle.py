from cv2 import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import array as arr

body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0)

points ={}
counter = 1

while True:
    _, img = cap.read()
    img = cv2.resize(img,(400,300),fx=0,fy=0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    body = body_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in body:
        cv2.rectangle(img, (x,y), (x*w, y*h), (255, 0, 0), 2)
        points[counter] = [x,y,w,h]

        counter = counter + 1

    
    cv2.imshow('img', img)
    
    

    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

