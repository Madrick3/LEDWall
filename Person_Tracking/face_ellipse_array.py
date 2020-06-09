from cv2 import cv2
import numpy as np

#Identify Webcam
cap = cv2.VideoCapture(0)

#Face Tracking Data
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


while True:
    '''Gathers data from webcam to identify face'''
    
    #Settings for Webcam
    _, img = cap.read()
    img = cv2.resize(img,(400,300),fx=0,fy=0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #Data
    class coordinates:
        ellipse_list=[]

    #Get face coordinate
    for (x, y, w, h) in faces:
        a, b, c, d = x, y, w, h
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)

    #Add to list
    ellipse = [a,b,c,d]
    coordinates.ellipse_list.append(ellipse)

    print(coordinates.ellipse_list)

    #Show webcam video with keypoints
    cv2.imshow('img', img)


    #Escape the Loop
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break


# %%
