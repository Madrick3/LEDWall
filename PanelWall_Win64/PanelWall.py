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

from multiprocessing import Process
from sys import exit
import time
import socket
import platform
import plistlib
import atexit

#TODO: Test this new version on linux distro
class PanelWall:

    userPlatform = platform.system()
    if(userPlatform == 'Linux'): 
        print("LEDWall/PanelWall_Win64: This module is not intended to be used with Linux Distros. Please use the Linux version of this module or use a Win64 Platform")
        exit(1)
    elif(userPlatform == 'Darwin'):
        print("LEDWall/PanelWall_Win64: This module is not intended to be used with MacOS. Please use the MacOS version of this module or use a Win64 Platform")
        exit(1)
    
    _pl = plistlib.readPlist("application.macosx/PanelWall.app/Contents/InfoTemplate.plist")
    _sock = socket.socket()
    _framerate = 15
    _period = 1/_framerate
    _starttime = time.time()
    _frameDuration = time.time() - _starttime
    _REDWALL = [[("255","0","0")]*10]*10
    _GREENWALL = [[("255","0","0")]*10]*10
    _BLUEWALL = [[("255","0","0")]*10]*10
    _screen = [[()]]
    _javaClient = socket.socket()
    _child = Process()

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
    }
    
    def __init__(self) -> None:
        """Creates and initializes the PanelWall python server and prepares a java client

        Runs at startup of module 
        """
        print("Creating Virtual Wall and creating a virtual server")
        HOST = "localhost"
        PORT = 2004
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
        self.f = open("panelScript.bat", "w")
        self.f.write('APPDIR=$(readlink -f "$0")\n')
        self.f.write('APPDIR=$(dirname "$APPDIR")\n')
        self.f.write('java -Djna.nosys=true -Djava.library.path="$APPDIR:$APPDIR/lib" -cp '
            '"$APPDIR:$APPDIR/lib/PanelWall.jar:$APPDIR/lib/core.jar:$APPDIR/lib/jogl-all.jar:' 
            '$APPDIR/lib/gluegen-rt.jar:$APPDIR/lib/jogl-all-natives-linux-aarch64.jar:'
            '$APPDIR/lib/gluegen-rt-natives-linux-aarch64.jar:$APPDIR/lib/nrserial.jar:'
            '$APPDIR/lib/PixelPusher.jar" PanelWall --this-goes-first thenThis')

    def bashCommand(self, String):
        print("method bashCommand is not implemented")


    def run(self) -> None:
        self.createBatch()
        command = "./application.macosx/PanelWall.app/Contents/MacOS/PanelWall"
        _child = Process(target=self.bashCommand, args=command)
        _child.start()
        (self._javaClient, info) = self._sock.accept()
        print("Socket Info: " + info)

    def updatePanel(self, digitalWall: [[(int, int, int)]]) -> bool:
        self._starttime = time.time()
        message = ""
        for row in digitalWall:
            message += "R"
            for entry in row:
                message += "C" + entry[0] + "," + entry[1] + "," + entry[2] + ","
        print("python is sending to java: " + message)
        sendthis = str.encode(message + "\n") #encode the message as bytes for sending to java - this can be improved
        self._javaClient.send(sendthis)
        self._frameDuration = time.time() - self._starttime
        
        if(self._frameDuration > 0):
            #print("frame had space to move: " + str(self.period - self.frameDuration))
            time.sleep(self._period - self._frameDuration)
        else:
            print("Frame took longer than determined period to update")
        print("flushing")
        message = "end\n"
        print("python is sending to java - flush: " + message)
        self._javaClient.send(str.encode(message)) #flush the stream
        return(True)
    
    def testUpdate(self) -> None:
        state = 0
        loop = 0
        while(True):
            if(state == 0):
                self._screen = self._REDWALL
                #loop+=1
            elif(state == 1):
                self._screen = self._GREENWALL
                #loop+=1
            else:
                self._screen = self._BLUEWALL
                #loop+=1
            if(loop == 100):
                print("newSttate")
                loop=0
                state+=1
                state%=3
            self.updatePanel(self._screen)

    def quitServer(self) -> None:
        self._child.join()
        self._javaClient.close()
        self._sock.close()

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
    
