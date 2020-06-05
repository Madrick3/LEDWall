#import PanelWall_Win64.PanelWall as Wall 
#from .PanelWall_Win64 import PanelWall as Wall
import PanelWall_Win64

def testTimingAndText():
    count = 0
    while True:
        count+=1
        myWall.start()
        myWall.text(str(count), 0, 96, 32)
        myWall.end()

def testLineCircleAndRect():
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
        drawLineCircleRect(fc, count)
        
def drawLineCircleRect(fc, count):
    myWall.start()
    myWall.text(str(fc), 0, 64, 32)
    myWall.text("Testing Circle, Line, and Rect", 0, 96, 32)
    myWall.circle(100,100,count*10)
    myWall.line(100,100,200+count*10,200+count*10)
    myWall.rectangle(200+count*10,200+count*10, 300+count*10, 300+count*10)
    myWall.end()        

def testMovingPoint():
    x = 0
    xStep = 5
    y = 0
    yStep = 5
    width = myWall.canvasWidth
    height = myWall.canvasHeight
    while True:
        x+=xStep
        y+=yStep
        if x > width:
            xStep = -5
        elif x < 0:
            xStep = 5
        if y > height:
            yStep = -5
        elif y < 0:
            yStep = 5   
        myWall.start() #start sending packet
        myWall.point(x, y) #add point to packet
        myWall.end() #end packet 


if __name__ == '__main__':
    myWall = PanelWall_Win64.PanelWall()
    myWall.defaultSettings()
    myWall.FrameCount = True
    myWall.synchronize = True #forces python to wait until java is ready to send new message
    myWall.run()
    #testMovingPoint()
    #testTimingAndText()
    testLineCircleAndRect()