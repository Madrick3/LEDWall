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
    noPanels:     (Boolean) True if pushing image to pixelpusher, false otherwise. Default: True
* stripsByRows:   (Boolean) True if strips are organized in rows instead of columns. Default: False 
    LEDMode:      (Boolean) True if we want images rendered in Processing as LEDS. Default: False
    FrameCount:   (Boolean) True if we want to display the current frame number. Default: False

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

    Accepts a string parameter to run in an os.system command. Kept outside of
    class instance to be used by child process.
    """
    #print("Child Process running command for Windows Application")

    os.system("cd %~dp0")
    os.system(commandString)

class PanelWall:

    TIMING_DEBUG = False
    PRINT_DEBUG = False
    _sock = socket.socket()
    _framerate = 30
    _period = 1/_framerate
    _starttime = time.time()
    _frameDuration = time.time() - _starttime
    _javaClient = socket.socket()
    _sync = False
    _message = ""
    _builtInApp = True

    _pl = plistlib.readPlist("PanelWall/application.macosx/PanelWall.app/Contents/InfoTemplate.plist")

    _path = "" #assumes that the directory "PanelWall_Win64" is in the same directory as the user's program
    

    _parameters = {
        "numPanelsX": (4, "--num-panels-x"),
        "numPanelsY": (3, "--num-panels-y"),
        "screenSaver": (1, "--screen-saver"),
        "canvasWidth": (800, "--canvas-width"),
        "canvasHeight": (600, "--canvas-height"),
        "noPanels": (True, "--no-panels"),
        "LEDMode": (True, "--led-mode"),
        "FrameCount": (False, "--frame-count"),
    }

    def __init__(self, debug:bool = False, builtInApp: bool = True) -> None:
        if(debug):
            self.debug()
        if(self.PRINT_DEBUG):
            print("Creating Virtual Wall and creating a virtual server")
        self._builtInApp = builtInApp
        userPlatform = platform.system()
        if(userPlatform == 'Linux'): 
            self.initLinux()
        elif(userPlatform == 'Darwin'):
            self.initMacOS()
        elif(userPlatform == 'Windows'):
            self.initWindows()
        else:
            print("Your operating system is not supported, please let a developer know of this problem and we will work with you to fix it!")
            exit()
    
    """Create a new file since the user is trying to use the wall"""
    def initMacOS(self) -> None:
        print("MacOS device found")
        HOST = "localhost"
        PORT = 2004
        self._sock.bind((HOST, PORT))
        self._sock.listen(1)
        atexit.register(self.quitServer)
    
    def initWindows(self) -> None:
        HOST = "localhost"
        PORT = 2004
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((HOST, PORT))
        self._sock.listen(1)
        atexit.register(self.quitServer)

    def initLinux(self) -> None:
        self.f = open("panelScript", "w")
        self.f.write('APPDIR=$(readlink -f "$0")\n')
        self.f.write('APPDIR=$(dirname "$APPDIR")\n')
        self.f.write('java -Djna.nosys=true -Djava.library.path="$APPDIR:$APPDIR/lib" -cp '
            '"$APPDIR:$APPDIR/lib/PanelWall.jar:$APPDIR/lib/core.jar:$APPDIR/lib/jogl-all.jar:' 
            '$APPDIR/lib/gluegen-rt.jar:$APPDIR/lib/jogl-all-natives-linux-aarch64.jar:'
            '$APPDIR/lib/gluegen-rt-natives-linux-aarch64.jar:$APPDIR/lib/nrserial.jar:'
            '$APPDIR/lib/PixelPusher.jar" PanelWall --this-goes-first thenThis')    

    def run(self) -> None:
        userPlatform = platform.system()
        if(userPlatform == 'Linux'): 
            self.runLinux()
        elif(userPlatform == 'Darwin'):
            self.runMacOS()
        elif(userPlatform == 'Windows'):
            self.runWindows()
        else:
            print("Your operating system is not supported, please let a developer know of this problem and we will work with you to fix it!")
            exit()
    
    def writeParameters(self) -> None:
        userPlatform = platform.system()
        if(userPlatform == 'Linux'): 
            self.writeParametersLinux()
        elif(userPlatform == 'Darwin'):
            self.writeParametersMacOS()
        elif(userPlatform == 'Windows'):
            self.createBatch()
        else:
            print("Your operating system is not supported, please let a developer know of this problem and we will work with you to fix it!")
            exit()

    def runWindows(self) -> None:
        self.writeParameters()
        command = self._path + ".\\PanelWall\\application.windows64\\panelScript.bat"
        if(self.PRINT_DEBUG):
            print("Starting Child Process to Manage Java Application")
        _child = Process(target=cmdPrompt, args=(command,))

        if self._builtInApp:
            _child.start()
       
        (self._javaClient, info) = self._sock.accept()
        if(self.PRINT_DEBUG):
            print("Socket Info: ", info)
    
    def createBatch(self) -> None:
        """Writes a batch file "panelScript.bat" that will be used as a java instance
        
        Creates a batch file that our PanelWall will execute in order to create
        a java instance. That java instance will either communicate with our 
        LED Wall at Pitt, or present to the user a digital representation of 
        what will be loaded on to the led wall.
        """
        if(self.PRINT_DEBUG):
            print("Creating Batch and writing")
        self.f = open("PanelWall\\application.windows64\\panelScript.bat", "w")
        self.f.write(' cd %~dp0\n')
        self.f.write('start %1PanelWall.exe')
        for paramPair in self._parameters.values():
            self.f.write(" " + paramPair[1] + " " + str(paramPair[0]))
        self.f.close()

    def runMacOS(self) -> None:
        self.writeParameters()
        command = "./PanelWall/application.macosx/PanelWall.app/Contents/MacOS/PanelWall"
        newpid = os.fork()
        if newpid == 0:
            print("Child Process")
            #print("child pwd")
            #os.system("pwd")
            if self._builtInApp:
                os.system(command)
        else:
            (self._javaClient, info) = self._sock.accept()
    
    def writeParametersMacOS(self) -> None:
        print("Parameters being used by the Wall: ")
        self._pl["JVMArguments"] = [] 
        for parameter in self._parameters:
            self._pl["JVMArguments"].append(self._parameters[parameter][1])
            self._pl["JVMArguments"].append(str(self._parameters[parameter][0]))
            print(" " + str(self._parameters[parameter][1]) + " " + str(self._parameters[parameter][0]))
        plistlib.writePlist(self._pl, "PanelWall/application.macosx/PanelWall.app/Contents/Info.plist")
    
    def runLinux(self) -> None:
        self.writeParameters()
        self.f.close()
        command = "chmod +x panelScript"
        os.system(command)

        command = "./panelScript"
        os.system(command)
    
    def writeParametersLinux(self) -> None:
        print("Parameters being used by the Wall: ")
        for parameter in self.parameters:
            self.f.write(" " + str(self.parameters[parameter][1]) + " " + str(self.parameters[parameter][0]))
            print(" " + str(self.parameters[parameter][1]) + " " + str(self.parameters[parameter][0]))

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
        if(self.PRINT_DEBUG):
            print("Server Sending: ", toSend)
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
    
    def ellipse(self, x:int, y:int, width:int, height:int):
        self._message = "ELL:"+ str(x) + " " + str(y) + " " + str(width) + " " + str(height) + "\r\n"
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