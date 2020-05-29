import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import java.util.*;
import java.net.Socket;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import processing.core.*;

DeviceRegistry registry;                
class TestObserver implements Observer { //This observer class verifies that a pixelpusher is connected to the raspberry pi through the network switch, it also gives us an easy way to connect to and interface with the pixelpusher
  public boolean hasStrips = false;
  public void update(Observable registry, Object updatedDevice) {
    println("Registry changed!");
    if (updatedDevice != null) {
      println("Device change: " + updatedDevice);
    }
    this.hasStrips = true;
  }
};

//MARK: Global Variable Declarations
int stride = 10; //Number of LEDS in a row, we snaked our LEDs so we must specially address each led 
float widthShrink, heightShrink, aspectRatio, x=0, y=0;
int xPanels = 4, yPanels = 3, imageWidth = 40, imageHeight = 30, canvasHeight = 30, canvasWidth = 40;
color colour = color(100, 100, 100);
boolean initializing = true, stripsByRows = false, sendToPanels = false;
int intensity = 255;
TestObserver testObserver;
PImage currentFrame;
int screenSaver = 0;
String filename = "image.jpg";

Boolean LEDMODE = false;
LED[][] LEDArray;

Interface pipe;

//MARK: Interaction Setting Variables
Space galaxy; //Space interaction
Rain downpour; //rain interaction
int rainLength, rainColor; 
Gradient gradient; //gradient screensaver
Pedestrian pedestrian; //pedestrian screensaver
int step; 

//MARK: SETTINGS
void settings() {
  String[] args = new String[]{"--num-panels-x", "4", "--num-panels-y", "3", "--screen-saver", "5", "--canvas-width", "800", "--canvas-height", "600", "--led-mode", "true"};
  for (int i = 0; i < args.length; i+=1 ) { //first we should determine what the command line arguments are: 
    System.out.println(args[i]);
    if (args[i].equals("--image-width")) {
      imageWidth = Integer.parseInt(args[i+1]); 
    } else if (args[i].equals("--image-height")) {
      imageHeight = Integer.parseInt(args[i+1]);
    } else if (args[i].equals("--num-panels-x")) {
      xPanels = Integer.parseInt(args[i+1]);
    } else if (args[i].equals("--num-panels-y")) {
      yPanels = Integer.parseInt(args[i+1]);
    } else if (args[i].equals("--screen-saver")) {
      screenSaver = Integer.parseInt(args[i+1]);
    } else if (args[i].equals("--canvas-width")) {
      canvasWidth = Integer.parseInt(args[i+1]);
    } else if (args[i].equals("--canvas-height")) {
      System.out.println("old canvas height!" + canvasHeight); 
      canvasHeight = Integer.parseInt(args[i+1]);
      System.out.println("new canvas height!" + canvasHeight);
    } else if (args[i].equals("--strips-by-rows")) {
      stripsByRows = Boolean.parseBoolean(args[i+1]);
    } else if (args[i].equals("--no-panels")) {
      sendToPanels = !Boolean.parseBoolean(args[i+1]);
      System.out.println("new sendToPanels!" + sendToPanels);
    } else if (args[i].equals("--send-to-panels")) {
      sendToPanels = !Boolean.parseBoolean(args[i+1]);
      System.out.println("new sendToPanels!" + sendToPanels);
    } else if (args[i].equals("--image-filename")) {
      filename = args[i+1];
    } else if (args[i].equals("--led-mode")) {
      LEDMODE = Boolean.parseBoolean(args[i+1]);
    } else if (args[i].equals("--rain-length")) {
      rainLength = Integer.parseInt(args[i+1]);
    } else if (args[i].equals("--rain-color")) {
      rainColor = Integer.parseInt(args[i+1]);
    }
  }
  System.out.println(canvasWidth + "" + canvasHeight);
  size(canvasWidth, canvasHeight);
  System.out.println("CanvasWidth: " + width + " and CanvasHeight: " + height);
}

//MARK: SETUP
/** Method: Function - Returns Void
 * This function is responsible for preparing the program to interface with the pixelpusher.
 * It specifies important values that we will use throughout the program,most of the globals are specified in this space.
 */
void setup() {
  //MARK: interaction setup
  galaxy = new Space(10);
  downpour = new Rain(2, color(0, 0, 255));
  gradient = new Gradient(1);
  pedestrian = new Pedestrian();

  //MARK: Display setup
  widthShrink = imageWidth/width;
  heightShrink = imageHeight/height;
  aspectRatio = width/height;
  frameRate(30); //determine the refresh rate we want the graphics to update at
  background(0); //initialize a black screen
  colorMode(RGB, 255, 255, 255, 255); //Specify the colormode of the pixels and their max values in RGBI mode (Red Green Blue Intensity)
  rectMode(CORNER);
  LEDArray = new LED[xPanels*stride][yPanels*stride];  //initialize the array of LEDS
  for (int x = 0; x < xPanels*stride; x++) {
    for (int y = 0; y < yPanels*stride; y++) {
      LEDArray[x][y] = new LED(x, y);
    }
  }
  
  //MARK: Python interface setup
  pipe = new Interface();


  //MARK: LEDWall Hardware Interface Setup
  registry = new DeviceRegistry(); //create the registry 
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  registry.setFrameLimit(1);
}

//MARK: DRAW
void draw() {
  if (testObserver.hasStrips || !sendToPanels) { //scrape for the strips and determine if we can send to the pixelpusher
    List<Strip> strips = registry.getStrips();
    registry.setExtraDelay(0);
    registry.startPushing();

    //Try to wipe the canvas completely
    stroke(0, 0, 0);
    fill(0, 0, 0);
    rect(0, 0, width, height); //Wipe the canvas and reload

    //THIS IS THE SECTION OF THE CODE WHICH READS IN THE IMAGE FROM THE DIRECTORY
    if (screenSaver == 0) { //python mode - we want to connect to a socket and 
      pipe.readMessageAndDraw(); //get the message from the pipe and see if we can print it
      pipe.sendReady();  
    } else if (screenSaver == 1 || screenSaver == 2) { //if(screenSaver == 1){ // doing a screensaver of some time
      downpour.update();
      downpour.draw();
    } else if (screenSaver == 3) {
      gradient.draw();
    } else if (screenSaver == 4) {
      pedestrian.draw();
    } else if (screenSaver == 5) {
      galaxy.update();
      galaxy.draw();
    }

    //If LEDMODE is true, then we can make the display look like LEDS on our LEDWall at benedum
    if (LEDMODE) { //changes the display to look a bit more like what it would like on the  ledwall at Pitt
      //First iterate through the screen so we can get the colors for each of the pixels
      for (int x = 0; x < xPanels*stride; x++) {
        for (int y = 0; y < yPanels*stride; y++) {
          LED curr = LEDArray[x][y];
          curr.setColor(0);
          //System.out.println(curr.toString());
        }
      }
      fill(0, 0, 0);
      stroke(0, 0, 0);
      rect(0, 0, width, height);
      //we drew the screen already so we need to wipe it and redraw the correct setup of LEDs
      for (int x = 0; x < xPanels*stride; x++) {
        for (int y = 0; y < yPanels*stride; y++) {
          LED curr = LEDArray[x][y];
          curr.draw();
        }
      }
    }


    //THIS IS THE SECTION OF CODE WHICH TRANSLATES THE CANVAS TO THE PHYSICAL PANEL
    // for every strip: we want to go through each LED and determine the location that LED should relate to on the canvas
    if (sendToPanels) {
      int stripOffsetX, stripOffsetY, panelPixelX, panelPixelY, canvasX, canvasY;
      float r, g, b;
      for (Strip strip : strips) { 
        if (stripsByRows) {
          stripOffsetX = 0;
          stripOffsetY = strip.getStripNumber() * height/yPanels;
        } else {
          stripOffsetX = strip.getStripNumber()*width/xPanels;
          stripOffsetY = 0;
        }
        for (int LEDIndex = 0; LEDIndex < strip.getLength(); LEDIndex++) { // for every pixel in the physical strip
          panelPixelX = LEDIndex % stride; 
          panelPixelY = LEDIndex / stride;          
          if (panelPixelY%2 == 1) {
            canvasX = (9-panelPixelX)*width/xPanels/stride + stripOffsetX;
            canvasY = panelPixelY*height/yPanels/stride + stripOffsetY;
          } else {
            canvasX = panelPixelX*width/xPanels/stride + stripOffsetX;
            canvasY = panelPixelY*height/yPanels/stride + stripOffsetY;
          }
          //System.out.println("LED: " + LEDIndex + " maps to canvas: " + canvasX + "-" + canvasY);

          color c = get(canvasX + width/xPanels/stride/2, canvasY + height/yPanels/stride/2);
          g = green(c);
          b = blue(c); 
          r = red(c);

          color newC = color(g, r, b);
          strip.setPixel(newC, LEDIndex);
        }
      }
    }
  }
}

public void pythonSerial() {
}

void mouseDragged() {
  if (screenSaver == 5) {
    galaxy.Sun.x = mouseX;
    galaxy.Sun.y = mouseY;
  }
}

void keyPressed() {
  if (key == 'q')
    LEDMODE = !LEDMODE;
  else if (key == 'a') {
    screenSaver--;
  } else if (key == 'd') {
    screenSaver++;
  } else if (key == 's') {
    frameRate(frameRate-1);
  } else if (key == 'w') {
    frameRate(frameRate+1);
  } else {
    if (screenSaver == 5) {
      galaxy = new Space(5+(int)random(10));
      stroke(0, 0, 0);
      fill(0, 0, 0);
      rect(0, 0, width, height); //Wipe the canvas and reload
    }
  }
}
