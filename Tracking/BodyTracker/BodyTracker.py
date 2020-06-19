import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

ksize = (15,15)
font = cv2.FONT_HERSHEY_SIMPLEX

def grayAndSmooth(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.blur(img, ksize)
    return img

# Video source - can be camera index number given by 'ls /dev/video*
# or can be a video file, e.g. '~/Video.avi'
cap = cv2.VideoCapture(0)
ret, background = cap.read()
background = grayAndSmooth(background)

cannyMin = 75

while(True):
    # Capture frame-by-frame
    ret, new = cap.read() 
    new = grayAndSmooth(new)
    delta = new - background
    ret, delta = cv2.threshold(delta, 127, 255, 0)
    # Display the resulting frame
    cv2.putText(new, str(cannyMin), (230, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    #_, delta = cv2.threshold(delta,127,255,cv2.THRESH_BINARY)
    #_, delta = cv2.threshold(delta, 200, 255, cv2.THRESH_BINARY)
    
    (width, height) = delta.shape
    contours = np.zeros(shape=[width, height], dtype=np.uint8)
    
    contours = cv2.Canny(delta, cannyMin, 150)
    thresh = cv2.threshold(contours, 255, 255, cv2.THRESH_BINARY)[1]

    """
    contours, cnts = cv2.findContours(delta, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    for c in cnts:
        print(c)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(contours, (x, y), (x + w, y + h), (255, 0, 0), 5)
        #cv2.rectangle(delta, (x, y), (x + w, y + h), (0, 0, 255), 2)
    """

    hstack = np.hstack((new, delta, contours, thresh))
    cv2.imshow("delta", hstack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('a'):
        cannyMin -= 1
    if cv2.waitKey(1) & 0xFF == ord('d'):
        cannyMin += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

