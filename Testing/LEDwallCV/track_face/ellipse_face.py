from cv2 import cv2
import numpy as np

#Identify Webcam
cap = cv2.VideoCapture(0)

#Face Tracking Data
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class coordinates:
    ellipse_list = []
    num_faces=0

def findFaceEllipse():
    #Data
    a, b, c, d = 0,0,0,0
    coordinates.ellipse_list=[]
    coordinates.num_faces=0

    #Settings for Webcam
    _, img = cap.read()
    img = cv2.resize(img,(400,300),fx=0,fy=0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #Get face coordinate
    for (x, y, w, h) in faces:
        coordinates.num_faces=1
        a, b, c, d = x, y, w, h

    #Add to list
    ellipse = [a,b,c,d]
    coordinates.ellipse_list.append(ellipse)


    #print(coordinates.ellipse_list)

#Show webcam video with keypoints
#cv2.imshow('img', img)
