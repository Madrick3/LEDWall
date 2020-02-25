# USAGE
# python detect_faces_video.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--prototxt", required=True,
# 	help="path to Caffe 'deploy' prototxt file")
# ap.add_argument("-m", "--model", required=True,
# 	help="path to Caffe pre-trained model")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
# 	help="minimum probability to filter weak detections")
# args = vars(ap.parse_args())

# load our serialized model from disk
# print("[INFO] loading model...")
# net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	orig = frame.copy()

	(rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

	# # loop over the detections
	# for i in range(0, detections.shape[2]):
	# 	# extract the confidence (i.e., probability) associated with the
	# 	# prediction
	# 	confidence = detections[0, 0, i, 2]
	#
	# 	# filter out weak detections by ensuring the `confidence` is
	# 	# greater than the minimum confidence
	# 	if confidence < args["confidence"]:
	# 		continue
	#
	# 	# compute the (x, y)-coordinates of the bounding box for the
	# 	# object
	# 	box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
	# 	(startX, startY, endX, endY) = box.astype("int")
	#
	# 	# draw the bounding box of the face along with the associated
	# 	# probability
	# 	text = "{:.2f}%".format(confidence * 100)
	# 	y = startY - 10 if startY - 10 > 10 else startY + 10
	# 	cv2.rectangle(frame, (startX, startY), (endX, endY),
	# 		(0, 0, 255), 2)
	# 	cv2.putText(frame, text, (startX, y),
	# 		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	# show the output frame
	cv2.imshow("Frame after compression", frame)
	cv2.imshow("Frame before compression", orig)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
