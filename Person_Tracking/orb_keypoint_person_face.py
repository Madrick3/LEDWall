#%%
from cv2 import cv2
import numpy as np

#Identify Webcam
cap = cv2.VideoCapture(0)

#Face Tracking Data
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


while True:
    '''Gathers data from webcam to identify keypoints
    Transforms keypoints into x and y coordinates 
    Filters coordinates by only locations inside a recognized face'''
    
    #Settings for Webcam
    _, img = cap.read()
    #img = cv2.resize(img,(400,300),fx=0,fy=0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #Using ORB to create keypoints
    orb = cv2.ORB_create()
    keypoints, descriptor = orb.detectAndCompute(gray, None)

    #Data for Loop
    i=0
    class coordinates:
        x_list=[]
        y_list=[]

    for i in range(len(keypoints)):
        '''Adds keypoint coordinates to a list'''
        x_kp = keypoints[i].pt[0]
        y_kp = keypoints[i].pt[1]
        for (x, y, w, h) in faces:
            if (x_kp < (x+w) and x_kp > x and y_kp < (h+y) and y_kp > y):
                coordinates.x_list.append(x_kp)
                coordinates.y_list.append(y_kp)

    print(coordinates)

    #Show webcam video with keypoints
    img = cv2.drawKeypoints(img, keypoints, descriptor)
    cv2.imshow('KeyPoints', img)


    #Escape the Loop
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break


# %%
