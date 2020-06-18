import PanelWall
from LEDwallCV.track_face import ellipse_face as face
from LEDwallCV.track_body import find_body as body
import time
from multiprocessing import Process

def testTimingAndText():
    count = 0
    while True:
        count+=1
        myWall.start()
        myWall.text(str(count), 0, 96, 32)
        myWall.end()

def testdrawEllipse():
    fc = 0
    count = 0
    step = 1
    while True:
        count+=step
        if(count < 0):
            step = 1
        elif(count > 10):
            step = -1
        fc+=1
        drawEllipse(fc, count) 


def drawEllipse(fc, count):
    myWall.start()
    myWall.text(str(fc), 0, 64, 32)
    myWall.text("Testing Tracking Face", 0, 96, 32)
    face.findFaceEllipse()
    ellipse_info = face.coordinates.ellipse_list
    number = face.coordinates.num_faces
    for i in range(number):
        myWall.ellipse(ellipse_info[i][0], ellipse_info[i][1], ellipse_info[i][2], ellipse_info[i][3])
        i=i+1
    myWall.end() 

def testdrawBody():
    fc = 0
    count = 0
    step = 1
    while True:
        count+=step
        if(count < 0):
            step = 1
        elif(count > 10):
            step = -1
        fc+=1
        drawBody(fc, count) 

def drawBody(fc, count):
    myWall.start()
    myWall.text(str(fc), 0, 64, 32)
    myWall.text("Testing Tracking Body", 0, 96, 32)
    body.findBodyLocation()
    body_info = body.coordinates.body_location
    number = body.coordinates.num_bodies
    for i in range(number):
        myWall.rectangle(body_info[i][0], body_info[i][1], body_info[i][2], body_info[i][3])
        i=i+1
    myWall.end() 

def multiprocess():
    p1 = Process(target = testdrawEllipse)
    p1.start()
    p2 = Process(target = testdrawBody)
    p2.start()

if __name__ == '__main__':
    myWall = PanelWall.PanelWall(debug = True, builtInApp = False)
    myWall.defaultSettings()
    myWall.FrameCount = True
    myWall.synchronize = True #forces python to wait until java is ready to send new message
    myWall.run()
    multiprocess()

