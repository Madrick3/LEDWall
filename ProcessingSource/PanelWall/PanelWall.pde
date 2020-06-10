import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import java.util.*;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.InetSocketAddress;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import processing.core.*;
import java.util.Scanner;

//MARK: Global Variable Declarations
int stride = 10; //number of LEDs 
int intensity = 255;
int screenSaver = 0;
int xPanels = 4;
int yPanels = 3;
int imageWidth = 40;
int imageHeight = 30;
int canvasHeight = 30;
int canvasWidth = 40;
float widthShrink;
float heightShrink;
float aspectRatio;
float x=0;
float y=0;
color colour = color(100, 100, 100);
boolean initializing = true;
boolean stripsByRows = false;
boolean sendToPanels = false;
Boolean LEDMODE = false;
boolean displayFrameCount = false;
String filename = "image.jpg";

PixelPusher hardware;
Interface pipe;
LEDArray LEDs;

//MARK: Interaction Setting Variables
Space galaxy; //Space interaction
Rain downpour; //rain interaction
int rainLength, rainColor; 
Gradient gradient; //gradient screensaver
Pedestrian pedestrian; //pedestrian screensaver

//MARK: SETTINGS
void settings() {
  String[] args = new String[]{"--num-panels-x", "4", "--num-panels-y", "3", "--screen-saver", "5", "--canvas-width", "800", "--canvas-height", "600", "--led-mode", "false", "--frame-count", "true"};
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
    } else if (args[i].equals("--frame-count")) {
      displayFrameCount = Boolean.parseBoolean(args[i+1]);
    }
  }
  size(canvasWidth, canvasHeight);
}

//MARK: SETUP
/** Method: Function - Returns Void
 * This function is responsible for preparing the program. Like in Arduino development, setup runs once at the start of the program.
 * It specifies important values that we will use throughout the program,most of the globals are specified in this space.
 * Screensavers and interactions probably want to initialize their class variables in this space.
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
  frameRate(45); //determine the refresh rate we want the graphics to update at
  background(0); //initialize a black screen
  colorMode(RGB, 255, 255, 255, 255); //Specify the colormode of the pixels and their max values in RGBI mode (Red Green Blue Intensity)
  rectMode(CORNER);

  //MARK: Backend Setup
  pipe = new Interface();
  LEDs = new LEDArray();
  hardware = new PixelPusher();
}

//MARK: DRAW
void draw() {
  if (hardware.canSendToStrips() || !sendToPanels) { //only draw if we can send to panels, or if we dont want to send to panels
    hardware.drawSetup();
    clearCanvas();

    //THIS IS THE SECTION OF THE CODE WHICH READS IN THE IMAGE FROM THE DIRECTORY
    if (screenSaver == 0) { //python mode - we want to connect to a socket and 
      pipe.readMessageAndDraw(); //get the message from the pipe and see if we can print it
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

    //DEBUG MESSAGES DRAWN TO CANVAS
    if (displayFrameCount) {
      drawDebugMessage(Integer.toString(frameCount), 1);
    }

    //FILTERS FOR CANVAS
    if (LEDMODE) { //changes the display to look a bit more like what it would like on the  ledwall at Pitt
      LEDs.draw();
    }

    //THIS IS THE SECTION OF CODE WHICH TRANSLATES THE CANVAS TO THE PHYSICAL PANEL
    if (sendToPanels) {
      hardware.pushToPixelPusher();
    }
  }
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
  } else if (key == ' ') {
    if (looping) noLoop();
    else         loop();
  } else if (key == '`') {
    stop();
  } else {
    if (screenSaver == 5) {
      galaxy = new Space(5+(int)random(10));
      clearCanvas();
    }
  }
}

void drawDebugMessage(String message, int row) {
  textSize(32);
  fill(255, 255, 255);
  text(message, 0, 32*row);
}

void clearCanvas() {
  stroke(0, 0, 0);
  fill(0, 0, 0);
  rect(0, 0, width, height); //Wipe the canvas and reload
}

int[] integerArrayListToArray(ArrayList<Integer> arr){
  int[] newArray = new int[arr.size()];
  int i = 0;
  for(int element: arr)
    newArray[i++] = element;
  return newArray;
}
