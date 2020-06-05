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
    //Do work for the screen
    myWall.updateScreen();
    
The developer should be careful to verify that the number of panels and
dimensions of these panels are accurate. If the physical arrangement of panels
is not the same as what is used in this software, incorrect behavior is likely
to occur.
"""

from multiprocessing import Process, Pipe, Lock
import subprocess
import os
from sys import exit
import time
import socket
import platform
import plistlib
import atexit

def cmdPrompt(commandString):
    """ Function used by child process to instantiate java/processing program

    Accepts a string parameter to run in an os.system command
    """
    os.system("cd %~dp0")
    os.system(commandString)

class PanelWall:

    userPlatform = platform.system()
    if(userPlatform == 'Linux'): 
        print("LEDWall/PanelWall_Win64: This module is not intended to be used with Linux Distros. Please use the Linux version of this module or use a Win64 Platform")
        exit(1)
    elif(userPlatform == 'Darwin'):
        print("LEDWall/PanelWall_Win64: This module is not intended to be used with MacOS. Please use the MacOS version of this module or use a Win64 Platform")
        exit(1)

    TIMING_DEBUG = False
    PRINT_DEBUG = False
    _sock = socket.socket()
    _framerate = 30
    _period = 1/_framerate
    _starttime = time.time()
    _frameDuration = time.time() - _starttime
    _REDWALL = [[("255","0","0")]*10]*10
    _GREENWALL = [[("255","0","0")]*10]*10
    _BLUEWALL = [[("255","0","0")]*10]*10
    _screen = [[()]]
    _javaClient = socket.socket()
    _sync = False
    
    _message = ""
    _path = "" #assumes that the directory "PanelWall_Win64" is in the same directory as the user's program
    digitalWall = bytearray()

    _parameters = {
        "imageWidth": (400, "--image-width"),
        "imageHeight": (300, "--image-height"),
        "numPanelsX": (4, "--num-panels-x"),
        "numPanelsY": (3, "--num-panels-y"),
        "screenSaver": (1, "--screen-saver"),
        "canvasWidth": (800, "--canvas-width"),
        "canvasHeight": (600, "--canvas-height"),
        "imageFilepath": ("testing.jpg", "--image-filename"),
        "noPanels": (True, "--no-panels"),
        "updateMode": (0, "--update-mode"),
        "LEDResolution": (True, "--lock-resolution"),
        "LEDMode": (True, "--led-mode"),
        "FrameCount": (False, "--frame-count"),
    }
    
    def __init__(self, debug: bool = False) -> None:
        """Creates and initializes the PanelWall python server and prepares a java client

        Runs at startup of module. If debug flag is given, initializes 
        debug parameters of object as true for its existence.
        """
        if(debug):
            self.debug()
        if(self.PRINT_DEBUG):
            print("Creating Virtual Wall and creating a virtual server")
        HOST = "localhost"
        PORT = 2004
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((HOST, PORT))
        self._sock.listen(1)
        atexit.register(self.quitServer)

    def createBatch(self) -> None:
        """Writes a batch file "panelScript.bat" that will be used as a java instance
        
        Creates a batch file that our PanelWall will execute in order to create
        a java instance. That java instance will either communicate with our 
        LED Wall at Pitt, or present to the user a digital representation of 
        what will be loaded on to the led wall.
        """
        self.f = open("PanelWall_Win64\\application.windows64\\panelScript.bat", "w")
        self.f.write(' cd %~dp0\n')
        self.f.write('start %1PanelWall.exe')
        for paramPair in self._parameters.values():
            self.f.write(" " + paramPair[1] + " " + str(paramPair[0]))
        self.f.close()

    def run(self) -> None:
        self.createBatch()
        command = self._path + ".\\PanelWall_Win64\\application.windows64\\panelScript.bat"
        _child = Process(target=cmdPrompt, args=(command,))
        _child.start()
       
        (self._javaClient, info) = self._sock.accept()
        print("Socket Info: ", info)
    
    #loop constantly sending a different set of points
    def testSocket(self):
        while True:
            print("sendingpoint")
            self.start()
            self.point(50,50)
            self.end()
            time.sleep(1)

    def testMovingPoint(self):
        x = 0
        xStep = 5
        y = 0
        yStep = 5
        width = self._parameters["canvasWidth"][0]
        height = self._parameters["canvasHeight"][0]
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
            self.start()
            self.point(x, y)
            self.end()
            

    #Sends current string in _message to socket
    def addMessage(self):
        toSend = bytes(self._message, encoding='utf8')
        print("Sending: ", toSend)
        self._javaClient.send(toSend)

    def start(self):
        self._starttime = time.time()
        self._message = "S\r\n"
        self.addMessage()

    def end(self):
        self._message = "E:\r\n"
        self.addMessage()
        if self._sync:
            time.sleep(self._frameDuration - (time.time()-self._starttime))

    def point(self, x:int, y:int):
        self._message = "P:" + str(x) + " " + str(y) + "\r\n" 
        self.addMessage()
    
    def rectangle(self, x0:int, y0:int, x1:int, y1:int):
        self._message = "R:"+ str(x0) + " " + str(y0) + " " + str(x1) + " " + str(y1) + "\r\n"
        self.addMessage()

    def line(self, x0:int, y0:int, x1:int, y1:int):
        self._message = "L:"+ str(x0) + " " + str(y0) + " " + str(x1) + " " + str(y1) + "\r\n"
        self.addMessage()

    def text(self, string: str, x:int, y:int, textSize:int):
        self._message = "T:" + str(x) + " " + str(y) + " " + str(textSize) + ":" + string + "\r\n"
        self.addMessage()

    def circle(self, x:int, y:int, radius:int):
        self._message = "C:" + str(x) + " " + str(y) + " " + str(radius) + "\r\n"
        self.addMessage()
    
    def debug(self) -> None:
        print("Python Client beginning debug")
        print("This message should not appear in production. Disable debug by eliminating/commenting any calls to '[User defined PanelWall Object].debug'")
        self.TIMING_DEBUG = True
        self.PRINT_DEBUG = True

    def quitServer(self) -> None:
        #self._child.join()
        self._javaClient.close()
        self._sock.close()
    
    def setPathToPanelWall_Win64(self, path: str):
        self._dirpath = path

    def defaultSettings(self):
        self.screenSaver = 0
        self.numPanelsX = 4
        self.numPanelsY = 3
        self.canvasWidth = 800
        self.canvasHeight = 600
        self.LEDMode = False
        self._framerate = 30
        self.synchronize = True

    @property
    def imageWidth(self) -> int:
        return self._parameters["imageWidth"][0]
    
    @imageWidth.setter
    def imageWidth(self, value: int) -> None:
        self._parameters["imageWidth"] = (value, "--image-width")
    
    @property
    def imageHeight(self) -> int:
        return self._parameters["imageHeight"][0]
    
    @imageHeight.setter
    def imageHeight(self, value: int) -> None:
        self._parameters["imageHeight"] = (value, "--image-height")
    
    @property
    def numPanelsX(self) -> int:
        return self._parameters["numPanelsX"][0]
    
    @numPanelsX.setter
    def numPanelsX(self, value: int) -> None:
        self._parameters["numPanelsX"] = (value, "--num-panels-x")
        
    @property
    def numPanelsY(self) -> int:
        return self._parameters["numPanelsY"][0]
    
    @numPanelsY.setter
    def numPanelsY(self, value: int) -> None:
        self._parameters["numPanelsY"] = (value, "--num-panels-y")
                
    @property
    def screenSaver(self) -> int:
        return self._parameters["screenSaver"][0]
    
    @screenSaver.setter
    def screenSaver(self, value: int) -> None:
        self._parameters["screenSaver"] = (value, "--screen-saver")
    
    @property
    def canvasWidth(self) -> int:
        return self._parameters["canvasWidth"][0]
    
    @canvasWidth.setter
    def canvasWidth(self, value: int) -> None:
        self._parameters["canvasWidth"] = (value, "--canvas-width")
        
    @property
    def canvasHeight(self) -> int:
        return self._parameters["canvasHeight"][0]
    
    @canvasHeight.setter
    def canvasHeight(self, value: int):
        self._parameters["canvasHeight"] = (value, "--canvas-height")
    
    @property
    def imageFilepath(self) -> str:
        return self._parameters["imageFilepath"][0]
    
    @imageFilepath.setter
    def imageFilepath(self, value: str):
        self._parameters["imageFilepath"] = (value, "--image-filename")

    @property
    def noPanels(self) -> str:
        return self._parameters["noPanels"][0]
    
    @noPanels.setter
    def noPanels(self, value: bool):
        self._parameters["noPanels"] = (value, "--no-panels")

    @property
    def sendToPanels(self) -> str:
        return self._parameters["noPanels"][0]
    
    @sendToPanels.setter
    def sendToPanels(self, value: bool) -> None:
        self._parameters["noPanels"] = (value, "--no-panels")

    @property
    def updateMode(self) -> int:
        return self._parameters["updateMode"][0]
    
    @updateMode.setter 
    def updateMode(self, value: int) -> None:
        self._parameters["updateMode"] = (value, "--update-mode")

    @property
    def LEDResolution(self) -> int:
        return self._parameters["LEDResolution"][0]
    
    @LEDResolution.setter 
    def LEDResolution(self, value: int) -> None:
        self._parameters["LEDResolution"] = (value, "--lock-resolution")

    @property
    def LEDMode(self) -> bool:
        return self._parameters["LEDMode"][0]
    
    @LEDMode.setter
    def LEDMode(self, value: bool) -> None:
        self._parameters["LEDMode"] = (value, "--led-mode")

    @property
    def synchronize(self) -> bool:
        return self._sync
    
    @synchronize.setter 
    def synchronize(self, value: bool) -> None:
        self._sync = value
        self._frameDuration = 1/self._framerate
    
    @property
    def FrameCount(self) -> bool:
        return self._parameters["FrameCount"][0]
    
    @FrameCount.setter 
    def FrameCount(self, value: bool) -> None:
        self._parameters["FrameCount"] = (value, "--frame-count")

"""
if __name__ == '__main__':
    myWall = PanelWall()
    myWall.defaultSettings()
    myWall.run()
    myWall.testMovingPoint()
"""