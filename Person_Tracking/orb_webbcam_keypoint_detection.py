#%%
from cv2 import cv2
import numpy as np

#Identify Webcam
cap = cv2.VideoCapture(0)

while True:
    #Settings for Webcam
    _, img = cap.read()
    img = cv2.resize(img,(400,300),fx=0,fy=0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Using ORB to create keypoints
    orb = cv2.ORB_create()
    keypoints, descriptor = orb.detectAndCompute(gray, None)
    img = cv2.drawKeypoints(img, keypoints, descriptor)


    #Show webcam video with keypoints
    cv2.imshow('KeyPoints', img)

    #Escape the Loop
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

# %%
