import PanelWall

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
    myWall.ellipse(300+count*10, 300+count*10, count*10, count*20)
    myWall.triangle(400, 400, 400+count*10, 400+count*10, 400-count*10, 400+count*10)
    myWall.shapeFromPoints(x=[100,150,200,300], y=[190, 100, 45, 400])
    myWall.end()        

if __name__ == '__main__':
    myWall = PanelWall.PanelWall(debug = True, builtInApp = True)
    myWall.defaultSettings()
    myWall.screenSaver = 3
    myWall.FrameCount = True
    myWall.synchronize = True #forces python to wait until java is ready to send new message
    myWall.run()
    #testLineCircleAndRect()