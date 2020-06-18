from LEDwallCV.track_face import ellipse_face as face
from LEDwallCV.track_body import find_body as body
import time
from multiprocessing import Process

def drawEllipse():
    start1 = time.time()
    print("Ellipse Start: ", start1)
    face.findFaceEllipse()
    ellipse_info = face.coordinates.ellipse_list
    print("Found Face: ", ellipse_info) 
    print(time.time()-start1)

def drawBody():
    start2 = time.time()
    print("Body Start: ", start2)
    body.findBodyLocation()
    body_info = body.coordinates.body_location
    print("Found Body: ", body_info)
    print(time.time()-start2)


def multiprocess():
    p1 = Process(target = drawEllipse)
    p1.start()
    p2 = Process(target = drawBody)
    p2.start()

if __name__ == '__main__':
    while True:
        multiprocess()
