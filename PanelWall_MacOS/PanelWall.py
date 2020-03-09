"""A module for controlling the LEDWall in the basement of Benedum Hall at the University of Pittsburgh

PanelWall is used to display images to a digital canvas and 'push' them
to the LED Wall. Primarily, this module is used to determine the behavior
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

Additionally, this program will create a local server to communicate with the java program.
#TODO: Create this interface

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


import os
import platform
import plistlib

 #TODO: Test this new version on linux distro
class PanelWall:

    userPlatform = platform.system()
    if(userPlatform == 'Linux'): 
        print("LEDWall/PanelWall_MacOS: This module is not intended to be used with Linux Distros. Please use the Linux version of this module or use a MacOS Platform")
        os._exit(1)
    elif(userPlatform == 'Windows'):
        print("LEDWall/PanelWall_MacOS: This module is not intended to be used with Windows. Please use the Windows version of this module or use a MacOS Platform")
        os._exit(1)
    
    pl = plistlib.readPlist("application.macosx/PanelWall.app/Contents/InfoTemplate.plist")

    parameters = {
        "imageWidth": (400, "--image-width"),
        "imageHeight": (300, "--image-height"),
        "numPanelsX": (4, "--num-panels-x"),
        "numPanelsY": (3, "--num-panels-y"),
        "screenSaver": (1, "--screen-saver"),
        "canvasWidth": (800, "--canvas-width"),
        "canvasHeight": (600, "--canvas-height"),
        "imageFilepath": ("testing.jpg", "--image-filename"),
        "noPanels": (True, "--no-panels")
    }
    
    """Create a new file since the user is trying to use the wall"""
    def __init__(self) -> None:
        print("Creating Virtual Wall")

    def writeParameters(self) -> None:
        print("Parameters being used by the Wall: ")
        self.pl["JVMArguments"] = [] 
        for parameter in self.parameters:
            self.pl["JVMArguments"].append(self.parameters[parameter][1])
            self.pl["JVMArguments"].append(str(self.parameters[parameter][0]))
            print(" " + str(self.parameters[parameter][1]) + " " + str(self.parameters[parameter][0]))
        plistlib.writePlist(self.pl, "application.macosx/PanelWall.app/Contents/Info.plist")
        #plistlib.dump(self.pl, self.fp, fmt=plistlib.FMT_XML, sort_keys=False, skipkeys=False)
        #print(self.pl)

    def run(self) -> None:
        self.writeParameters()
        command = "./application.macosx/PanelWall.app/Contents/MacOS/PanelWall"
        os.system(command)

    """"""
    #def updatePanel(self) -> bool:

    
    @property
    def imageWidth(self) -> int:
        return self.parameters["imageWidth"][0]
    
    @imageWidth.setter
    def imageWidth(self, value: int) -> None:
        self.parameters["imageWidth"] = (value, "--image-width")
    
    @property
    def imageHeight(self) -> int:
        return self.parameters["imageHeight"][0]
    
    @imageHeight.setter
    def imageHeight(self, value: int) -> None:
        self.parameters["imageHeight"] = (value, "--image-height")
    
    @property
    def numPanelsX(self) -> int:
        return self.parameters["numPanelsX"][0]
    
    @numPanelsX.setter
    def numPanelsX(self, value: int) -> None:
        self.parameters["numPanelsX"] = (value, "--num-panels-x")
        
    @property
    def numPanelsY(self) -> int:
        return self.parameters["numPanelsY"][0]
    
    @numPanelsY.setter
    def numPanelsY(self, value: int) -> None:
        self.parameters["numPanelsY"] = (value, "--num-panels-y")
                
    @property
    def screenSaver(self) -> int:
        return self.parameters["screenSaver"][0]
    
    @screenSaver.setter
    def screenSaver(self, value: int) -> None:
        self.parameters["screenSaver"] = (value, "--screen-saver")
    
    @property
    def canvasWidth(self) -> int:
        return self.parameters["canvasWidth"][0]
    
    @canvasWidth.setter
    def canvasWidth(self, value: int) -> None:
        self.parameters["canvasWidth"] = (value, "--canvas-width")
        
    @property
    def canvasHeight(self) -> int:
        return self.parameters["canvasHeight"][0]
    
    @canvasHeight.setter
    def canvasHeight(self, value: int):
        self.parameters["canvasHeight"] = (value, "--canvas-height")
    
    @property
    def imageFilepath(self) -> str:
        return self.parameters["imageFilepath"][0]
    
    @imageFilepath.setter
    def imageFilepath(self, value: str):
        self.parameters["imageFilepath"] = (value, "--image-filename")

    @property
    def noPanels(self) -> str:
        return self.parameters["noPanels"][0]
    
    @noPanels.setter
    def noPanels(self, value: bool):
        self.parameters["noPanels"] = (value, "--no-panels")

    @property
    def sendToPanels(self) -> str:
        return self.parameters["noPanels"][0]
    
    @noPanels.setter
    def sendToPanels(self, value: bool):
        self.parameters["noPanels"] = (value, "--no-panels")

myWall = PanelWall()

myWall.screenSaver = 3
myWall.numPanelsX = 1
myWall.numPanelsY = 1
myWall.canvasWidth = 100
myWall.canvasHeight = 100
myWall.run()
