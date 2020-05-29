import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import com.heroicrobot.dropbit.registry.*; 
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel; 
import com.heroicrobot.dropbit.devices.pixelpusher.Strip; 
import java.util.*; 
import java.net.Socket; 
import java.io.DataInputStream; 
import java.io.DataOutputStream; 
import java.io.InputStreamReader; 
import processing.core.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class PanelWall extends PApplet {











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
int colour = color(100, 100, 100);
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
public void settings() {
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
public void setup() {
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
public void draw() {
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

          int c = get(canvasX + width/xPanels/stride/2, canvasY + height/yPanels/stride/2);
          g = green(c);
          b = blue(c); 
          r = red(c);

          int newC = color(g, r, b);
          strip.setPixel(newC, LEDIndex);
        }
      }
    }
  }
}

public void pythonSerial() {
}

public void mouseDragged() {
  if (screenSaver == 5) {
    galaxy.Sun.x = mouseX;
    galaxy.Sun.y = mouseY;
  }
}

public void keyPressed() {
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

public class Gradient {
  int r=255, g=0, b=0, colorState=0, step;

  public Gradient(int step) {
    this.step = step;
  }

  public void draw() {
    stroke(r, g, b);
    fill(r, g, b);
    rect(0, 0, width, height); //Wipe the canvas and reload
    if (colorState == 0) {
      g+=step;
      if (g>=255) colorState = 1;
    }
    if (colorState == 1) {
      r-=step;
      if (r<=0) colorState = 2;
    }
    if (colorState == 2) {
      b+=step;
      if (b>=255) colorState = 3;
    }
    if (colorState == 3) {
      g-=step;
      if (g<=0) colorState = 4;
    }
    if (colorState == 4) {
      r+=step;
      if (r>=255) colorState = 5;
    }
    if (colorState == 5) {
      b-=step;
      if (b<=0) colorState = 0;
    }
  }
}
public class Interface {
  public Socket socket = null;
  public PrintWriter out;
  public BufferedReader in;
  public DataOutputStream pythonOut = null;
  public boolean socketPass = false;

  final char startChar = 's';
  final char endChar = 'e';
  final char pointChar = 'p';
  final char linechar = 'l';
  final char coordDelim = ',';
  final char ready = 'q';  

  public Interface() {
    try {
      socket = new Socket("localhost", 2004);
      out = new PrintWriter(socket.getOutputStream(), true);
      in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
      socketPass = true;
    } 
    catch(Exception e) {
      println(e); 
      socketPass = false;
    };
  }

  public void readMessageAndDraw(){
    boolean keepGoing = true, start = false;
    char readin;
    String raw;
    ArrayList<Integer> x;
    ArrayList<Integer> y;
    try {
      while (keepGoing) {
        raw = in.readLine();  
        x = new ArrayList<Integer>();
        y = new ArrayList<Integer>();
        if (raw == "E") {
          start = false;
          continue;
        }
        if (raw == "S") {
          start = true;
        }
        if (raw == "P") {
          int type = 1;
          x.add(Integer.parseInt(in.readLine()));
          y.add(Integer.parseInt(in.readLine()));
          new drawing(1, x.toArray(new Integer[x.size()]), y.toArray(new Integer[y.size()]));
        }
        if (raw == "L") {
          int type = 2;
          x.add(Integer.parseInt(in.readLine()));
          y.add(Integer.parseInt(in.readLine()));
          x.add(Integer.parseInt(in.readLine()));
          y.add(Integer.parseInt(in.readLine()));
          new drawing(1, x.toArray(new Integer[x.size()]), y.toArray(new Integer[y.size()]));
        }
      }
    }  
    catch(Exception e) {
      print("Something went wrong");
    }
  }
  
  public void sendReady(){
    try{
      out.write("*");  
    } catch(Exception e){
      print("Something went wrong with send");
    }
  }
}

public class LED {
  public int x, y, xi, yi, diameter, intensity;
  public int colour;

  public LED(int x, int y) {
    this.x = (x+1)*20-10;
    this.y = (y+1)*20-10;
    xi = x*20;
    yi = y*20;
    diameter = 5;
  }

  public void setColor(int dim) {
    if (dim > 255)
      dim = 255;
    float meanR = 0, meanG= 0, meanB = 0;
    int numPixels = width/xPanels/stride * height/yPanels/stride;
    for (int i = 0; i < width/xPanels/stride; i++) {
      for (int j = 0; j < height/yPanels/stride; j++) {
        colour = get(xi+i, yi+j);
        float r = red(colour);
        float g = green(colour);
        float b = blue(colour);
        meanR += r;
        meanG += g;
        meanB += b;
      }
    }
    meanR/=numPixels;
    meanG/=numPixels;
    meanB/=numPixels;
    meanR-= dim;
    meanG-= dim;
    meanB-= dim;
    //System.out.println("Average color for this: " + meanR + " " + meanG + " " + meanB);
    this.colour = color(meanR, meanG, meanB);
  }

  public void draw() {
    fill(red(colour), green(colour), blue(colour));
    stroke(red(colour), green(colour), blue(colour));
    circle(x, y, diameter);
  }

  public String toString() {
    return("LED[" + x + "][" + y + "] with color: " + colour);
  }
}
public class Pedestrian{
  int state;
  int circleX=0, circleY = 150; 
  int circleDirection = 1, circleIntensity = 255, circleIntensityDirection = -1;
  int circleLegTilt = 0, circleLegTiltCounter = 0; //walker screensaver
  
  public Pedestrian(){
    state = 0;
  }
  
  public void draw(){
    //This screensaver animates a person walking from left to right and then back to left
      ///stroke(255-circleIntensity,255-circleIntensity,255-circleIntensity); //We stopped using this because we didnt want the random dimming
      //fill(255-circleIntensity,0,255-circleIntensity);
      stroke(255, 255, 255);
      fill(255, 0, 255);
      if (state == 0) {
        circleLegTilt = 0;
        if (circleLegTiltCounter == 5) {
          state = 1; 
          circleLegTiltCounter=0;
        }
      } else if (state == 1) {
        circleLegTilt = 1;
        if (circleLegTiltCounter == 5) {
          state = 2; 
          circleLegTiltCounter=0;
        }
      } else if (state == 2) {
        circleLegTilt = 0;
        if (circleLegTiltCounter == 5) {
          state = 3; 
          circleLegTiltCounter=0;
        }
      } else if (state == 3) {
        circleLegTilt = -1;
        if (circleLegTiltCounter == 5) {
          state = 0; 
          circleLegTiltCounter=0;
        }
      }
      circleLegTiltCounter++;


      if (circleX >= 800) {
        circleDirection = -1;
      }
      if (circleX < 0) {
        circleDirection = 1;
      }
      switch(circleLegTilt) {
      case 0: //no tilts at all
        quad(circleX-70+50, circleY+200, circleX-70+50+50, circleY+200, circleX-70+50+50, circleY+200+150, circleX-70+50, circleY+200+150); //left leg standing straight up and down
        quad(circleX+20-50, circleY+200, circleX+20+50-50, circleY+200, circleX+20+50-50, circleY+200+150, circleX+20-50, circleY+200+150); //right leg standing straight up and down
        break;
      case 1: //right leg forward
        quad(circleX-70+15+50, circleY+200-35, circleX-70+50+50, circleY+200, circleX-70+35-106+50, circleY+200+150-35, circleX-70-106+50, circleY+200+150-70); //left leg moving to the right
        quad(circleX+20-50, circleY+200, circleX+20+50-15-50, circleY+200-35, circleX+20+35+106-50, circleY+200+150-70, circleX+20+106-50, circleY+200+150-35); //right leg moving to the left
        break;
      case -1: //
        quad(circleX-70+50, circleY+200, circleX-70+35+50, circleY+200-35, circleX-70+35+106+50, circleY+200+150-70, circleX-70+106+50, circleY+200+150-35); //left leg goes to the right
        quad(circleX+20+15-50, circleY+200-35, circleX+20+50-50, circleY+200, circleX+20+35-106-50, circleY+200+150-35, circleX+20-106-50, circleY+200+150-70); //right leg goes to the left
        break;
      }
      triangle(circleX, circleY, circleX-50, circleY+200, circleX+50, circleY+200);
      circle(circleX, circleY, 100);
      circleX += (circleDirection * 15);
  }
}
public class Rain {
  int rainLength = 3, newRainStart;
  ArrayList<drop> droplets;
  int rain_color = color(0, 128, 255);

  public Rain(int rainLength, int rain_color) {
    droplets = new ArrayList<drop>(height);
    this.rainLength = rainLength;
    this.rain_color = rain_color;
  }

  public void update() {
    newRainStart = (int)random(width/(width/xPanels/stride));
    newRainStart = newRainStart*(width/xPanels/stride);
    drop newRain = new drop(newRainStart, 0, 1 + (int) random(rainLength));
    droplets.add(newRain);
    newRain = new drop(newRainStart, 0, 1 + (int) random(rainLength));
    droplets.add(newRain);
    newRain = new drop(newRainStart, 0, 1 + (int) random(rainLength));
    droplets.add(newRain);
  }

  public void draw() {
    for (int i = 0; i < droplets.size(); i++) {
      drop d = droplets.get(i);
      d.draw(rain_color);
    }
  }
}

class drop {
  public int dropLength, x, y, radius; //x and y are the coordinates for the top left corner, radius is the size of the square we are drawing in pixels
  public drop(int x, int y, int dropLength) {
    this.x = x;
    this.y = y;
    this.radius = width/xPanels/stride;
    this.dropLength = dropLength;
  } 

  public String toString() {
    return ("Rain: [" + this.x + "," + this.y + "]");
  }

  public void draw(int colour) {
    fill(colour);
    rectMode(CORNER);
    rect(x, y, radius, radius);
    y = y + radius*dropLength/2;
    for (int j = 0; j < dropLength; j++) {
      stroke(0, j*25, 127-j*25);
      rect(x, y - j*radius, radius, radius);
    }
  }
}
static public float pi = 3.14159f;
static public float G = 10;
final public int[] planetColors = {color(255,0,0), color(0,255,0), color(0,0,255), color(255,0,255), color(0,128,255)};// color(#FFC081),};// color(#FF4DC1)};

public class Space{
  ArrayList<Planet> SolarSystem;
  ArrayList<star> stars;
  Planet Sun = new Planet(width/2, height/2);
  
  public Space(int numPlanets){
    SolarSystem = new ArrayList();
    for(int i = 0; i < numPlanets; i++){
      SolarSystem.add(new Planet(SolarSystem, Sun));
    }
    stars = new ArrayList();
    int numStars = 100 + (int) random(width/1600);
    for(int i = 0; i < numStars; i++)
      stars.add(new star());
  }
  
  public void update(){
    for(Planet p: SolarSystem){
      p.update();
    }
    for(int i = 0; i < SolarSystem.size(); i++){
      if(SolarSystem.get(i).skip)
        SolarSystem.remove(i);
    }
    
  }
  
  public void draw(){
    for(star s: stars){
      s.draw();
    }
    Sun.draw();
    for(Planet p: SolarSystem){
      p.draw();
    }
    
  }
  
  public class star{
    int x, y, radius, intensity;
    public star(){
      x = (int) random(width);
      y = (int) random(height);
      radius = 5 + (int) random(10);
      intensity = 128 + (int) random(128);
    }
    
    public void draw(){
      fill(intensity, intensity, intensity);
      stroke(intensity, intensity, intensity);
      circle(x,y, radius);
    }
  }
  
  public class Planet{
    PVector velocity, acceleration;
    float x, y, radius, ran;
    float mass;
    int colour;
    int colorIndex;
    ArrayList<Planet> SolarSystem;
    Planet Sun;
    Boolean skip = false;
    
    public Planet(ArrayList<Planet> SolarSystem, Planet Sun){
      x = (int) random(width);
      y = (int) random(height);
      radius = 15 + width/100*(int)random(5);
      colorIndex = (int) random(planetColors.length);
      colour = planetColors[colorIndex];
      mass = radius;
      this.SolarSystem = SolarSystem;
      this.Sun = Sun;
      
      acceleration = new PVector(0,0);
      velocity = getInitialVelocity();
    }
    
    public Planet(int x, int y){
      this.x = x;
      this.y = y;
      radius = width/16;
      colour = color(255, 255, 255);
      mass = 300;
      acceleration = new PVector(0,0);
      velocity = new PVector(0,0);
      this.Sun = this;
    }
    
    public PVector getInitialVelocity(){
      PVector distance, vi = new PVector(0,0);
      distance = new PVector(this.x-Sun.x, this.y-Sun.y);
      float vMag = sqrt(G * Sun.mass / distance.mag())*0.85f;
      vi.set(-1*vMag*distance.y/distance.mag(), vMag*distance.x/distance.mag());
      return vi; 
    }
    
    public PVector partialAccel(Planet p){
      PVector acceleration, distance;
      float a;
      distance = new PVector(this.x - p.x, this.y - p.y);
      //distance = new PVector(p.x-this.x, p.y-this.y);
      if(distance.mag() < this.radius/2 || distance.mag() < p.radius/2){
        merge(p);
        
        acceleration = new PVector(0,0);
        return acceleration;
      }
      a = G*p.mass/distance.magSq();
      acceleration = new PVector(a*-1*distance.x/distance.mag(), a*-1*distance.y/distance.mag());
      return acceleration;
    }
    
    public void updateAcceleration(){
      acceleration = new PVector(0,0);
      acceleration.add(partialAccel(Sun));
      for(Planet p: SolarSystem){
        if((p != this) && !p.skip){
          acceleration.add(partialAccel(p));
        }    
      }
    }
    
    public void merge(Planet p){
      p.radius = pow(radius, 2) + pow(p.radius, 2);
      p.radius = sqrt(p.radius);
      float temp = mass;
      p.mass += mass;
      velocity.x*=mass/(mass+p.mass); velocity.y*=mass/(mass+p.mass); p.velocity.x*=mass/(mass+p.mass); p.velocity.y*=mass/(mass+p.mass);
      p.velocity.add(velocity);
      p.colour = color((red(p.colour) + red(this.colour))/2, (green(p.colour) + green(this.colour))/2, (blue(p.colour) + blue(this.colour))/2);
      skip = true;
    }
  
    public void update(){
      updateAcceleration();
      acceleration.x/=2;
      acceleration.y/=2;
      velocity.add(acceleration.x, acceleration.y);
      x = x + velocity.x/2 + acceleration.x/4; 
      y = y + velocity.y/2 + acceleration.y/4;
    }
    
    public void draw(){
      float diamond = 2*radius/3;
      stroke(255,0,0);
      line(this.x, this.y, this.x+acceleration.x*10, this.y+acceleration.y*10);
      stroke(0,255,0);
      line(this.x, this.y, this.x+velocity.x*10, this.y+velocity.y*10);
      
      stroke(255,255,255);
      fill(colour);
      rectMode(CORNERS);
      
      if(frameCount%(15+(int)random(30)) ==0)
        ran = random(pi/3) + 0.1f;
      if(this.Sun == this){
        stroke(255,255,255);
        fill(red(colour)%55+200, green(colour)%55+200, blue(colour)%55+200);
        rectMode(CORNERS);
        rect(x-radius/2, y-radius/2, x+radius/2, y+radius/2);
        quad(x, y-diamond, x+diamond, y, x, y+diamond, x-diamond, y);
        quad(x+diamond*cos(ran),y+diamond*sin(ran), x+diamond*cos(ran + pi/2),y+diamond*sin(ran + pi/2), x+diamond*cos(ran + pi),y+diamond*sin(ran + pi), x+diamond*cos(ran + 3*pi/2),y+diamond*sin(ran + 3*pi/2));
      } else {
        circle(x,y,radius);
      }
    }
    
  }
  
}
public class drawing {
  int type;
  int[] x, y;
  int colour = color(255, 0, 255);
  
  public drawing(int t, Integer[] x, Integer[] y) {
    stroke(255,255,255);
    fill(colour);
    if ( t != x.length || t != y.length){
      print("Packet Error");
    } else if (t == 1){
      circle(x[0], y[0], 5);
    } else if (t == 2){
      circle(x[0], y[0], 5);
      circle(x[1], y[1], 5);
      line(x[0], y[0], x[1], y[2]);
    }
  }
}

  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "PanelWall" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
