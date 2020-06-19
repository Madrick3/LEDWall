import PanelWall
from .LEDwallCV.track_face import ellipse_face as face
import time

def testTimingAndText():
    count = 0
    while True:
        count+=1
        myWall.start()
        myWall.text(str(count), 0, 96, 32)
        myWall.end()

def testdrawEllipse():
    fc = 0
    while True:
        fc+=1
        print("INFO: Starting Face Track...")
        drawEllipse(fc) 


def drawEllipse(fc):
    start = time.time()
    myWall.start()
    myWall.text(str(fc), 0, 64, 32)
    myWall.text("Testing Tracking Face", 0, 96, 32)
    face.findFaceEllipse()
    ellipse_info = face.coordinates.ellipse_list
    #number = face.coordinates.num_faces
    #for i in range(number):
        #myWall.ellipse(ellipse_info[i][0], ellipse_info[i][1], ellipse_info[i][2], ellipse_info[i][3])
        #i=i+1
    #print("The ellispe is located: ", ellipse_info[0][0], ellipse_info[0][1], ellipse_info[0][2], ellipse_info[0][3])
    myWall.ellipse(ellipse_info[0], ellipse_info[1], ellipse_info[2], ellipse_info[3]) 
    print("Time to Complete: ", time.time()-start)
    myWall.end()
    


if __name__ == '__main__':
    myWall = PanelWall.PanelWall(debug = True, builtInApp = False)
    myWall.defaultSettings()
    myWall.FrameCount = True
    myWall.synchronize = True #forces python to wait until java is ready to send new message
    myWall.run()
    testdrawEllipse()
    