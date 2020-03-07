"""A module for controlling the LEDWall in the basement of Benedum Hall at the University of Pittsburgh

PanelWall is used to display images to a digital canvas and 'push' them
to the LED Wall. This moduleprimarily is used to determine the behavior
of the LED Wall, (e.g. The number and arrangement of panels, dynamic or
static operation, dimensions of the digital canvas, etc.).
This module interfaces with a Java program and sends user defined parameters
to the executable. The following parameters are currently supported:
    canvasWidth:  (int) The width in pixels of the digital canvas. Default: 400
    canvasHeight: (int) The height in pixels of the digital canvas. Default: 300
    numPanelsX:   (int) The width in panels of the physical canvas. Default: 4
    numPanelsY:   (int) The height in panels of the physical canvas. Default: 3
    screenSaver:  (int) The type of screenSaver operation for the canvas. Default: 1
    imageFilepath:(Str) The relative path to the file that we are trying to print. Default: "testing.jpg"
    imageWidth:   (int) The width in pixels of the image file supplied. Default: 400
    imageHeight:  (int) The height in pixels of the image file supplied. Default: 300

The following is a simple example usage which assumes only 1 panel and iterates through the RGB spectrum:
    myWall = PanelWall()
    myWall.screenSaver = 3
    myWall.numPanelsX = 1
    myWall.numPanelsY = 1
    myWall.canvasWidth = 800
    myWall.canvasHeight = 800
    myWall.run()
    
The developer should be careful to verify that the number of panels and
dimensions of these panels are accurate. If the physical arrangement of panels
is not the same as what is used in this software, incorrect behavior is likely
to occur.
"""

#!/usr/bin/python 3
import os
import platform

class PanelWall:
    userPlatform = platform.system()
    if(userPlatform == 'Darwin'): 
        print("This module is not intended to be used with MacOS. Please use the MacOS version of this module or use a Linux Platform")
    elif(userPlatform == 'Windows'):
        print("This module is not intended to be used with Windows. Please use the Windows version of this module or use a Linux Platform")
    
    f = open("garbagescript.trash","w")
    
    parameters = {
        "imageWidth": 400,
        "imageHeight": 300,
        "numPanelsX": 4,
        "numPanelsY": 3,
        "screenSaver": 1,
        "canvasWidth": 800,
        "canvasHeight": 600,
        "imageFilepath": "testing.jpg",
        }
    
    parameterNames = {
        "imageWidth": "--image-width",
        "imageHeight": "--image-height",
        "numPanelsX": "--num-panels-x",
        "numPanelsY": "--num-panels-y",
        "screenSaver": "--screen-saver",
        "canvasWidth": "--canvas-width",
        "canvasHeight": "--canvas-height",
        "imageFilepath": "--image-filename",
        }
    
    changed = {
        "imageWidth": False,
        "imageHeight": False,
        "numPanelsX": False,
        "numPanelsY": False,
        "screenSaver": False,
        "canvasWidth": False,
        "canvasHeight": False,
        "imageFilepath": False,
        }

    def __init__(self):
        self.f = open("panelScript", "w")
        self.f.write('APPDIR=$(readlink -f "$0")\n')
        self.f.write('APPDIR=$(dirname "$APPDIR")\n')
        self.f.write('java -Djna.nosys=true -Djava.library.path="$APPDIR:$APPDIR/lib" -cp '
            '"$APPDIR:$APPDIR/lib/PanelWall.jar:$APPDIR/lib/core.jar:$APPDIR/lib/jogl-all.jar:'
            '$APPDIR/lib/gluegen-rt.jar:$APPDIR/lib/jogl-all-natives-linux-aarch64.jar:'
            '$APPDIR/lib/gluegen-rt-natives-linux-aarch64.jar:$APPDIR/lib/nrserial.jar:'
            '$APPDIR/lib/PixelPusher.jar" PanelWall --this-goes-first thenThis ')    
    
    def writeParameters(self):
        print("Parameters being used by the Wall")
        for prop in self.changed:
            if(self.changed[prop]):
                self.f.write(str(self.parameterNames[prop]) + " " + str(self.parameters[prop]) + " ")
                print(str(self.parameterNames[prop]) + " " + str(self.parameters[prop]) + " ")

    def run(self):
        self.writeParameters()
        self.f.close()
        command = "chmod +x panelScript"
        os.system(command)

        command = "./panelScript"
        os.system(command)
    
    @property
    def imageWidth(self):
        return self.parameters["imageWidth"]
    
    @imageWidth.setter
    def imageWidth(self, value):
        self.parameters["imageWidth"] = value
        self.changed["imagewidth"] = True
    
    @property
    def imageHeight(self):
        return self.parameters["imageHeight"]
    
    
    @imageHeight.setter
    def imageHeight(self, value):
        self.parameters["imageHeight"] = value
        self.changed["imageHeight"] = True
    
    @property
    def numPanelsX(self):
        return self.parameters["numPanelsX"]
    
    @numPanelsX.setter
    def numPanelsX(self, value):
        self.parameters["numPanelsX"] = value
        self.changed["numPanelsX"] = True
        
    @property
    def numPanelsY(self):
        return self.parameters["numPanelsY"]
    
    @numPanelsY.setter
    def numPanelsY(self, value):
        self.parameters["numPanelsY"] = value
        self.changed["numPanelsY"] = True
                
    @property
    def screenSaver(self):
        return self.parameters["screenSaver"]
    
    @screenSaver.setter
    def screenSaver(self, value):
        self.parameters["screenSaver"] = value
        self.changed["screenSaver"] = True
    
    @property
    def canvasWidth(self):
        return self.parameters["canvasWidth"]
    
    @canvasWidth.setter
    def canvasWidth(self, value):
        self.parameters["canvasWidth"] = value
        self.changed["canvasWidth"] = True
        
    @property
    def canvasHeight(self):
        return self.parameters["canvasHeight"]
    
    @canvasHeight.setter
    def canvasHeight(self, value):
        self.parameters["canvasHeight"] = value
        self.changed["canvasHeight"] = True
    
    @property
    def imageFilepath(self):
        return self.parameters["imageFilepath"]
    
    @imageFilepath.setter
    def imageFilepath(self, value):
        self.parameters["imageFilepath"] = value
        self.changed["imageFilepath"] = True

myWall = PanelWall()
myWall.screenSaver = 3
myWall.numPanelsX = 1
myWall.numPanelsY = 1
myWall.canvasWidth = 100
myWall.canvasHeight = 100
myWall.run()
