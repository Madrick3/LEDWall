import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import java.util.*;
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

class Rain{
  public int x, y, radius; //x and y are the coordinates for the top left corner, radius is the size of the square we are drawing in pixels
  public Rain(int x, int y){
    this.x = x;
    this.y = y;
    this.radius = width/xPanels/stride;
  } 
  
  public String toString(){
    return ("Rain: [" + this.x + "," + this.y + "]"); 
  }
}

class LED{
  public int x, y, xi, yi, diameter, intensity;
  public color colour;
  
  public LED(int x, int y){
    this.x = (x+1)*20-10;
    this.y = (y+1)*20-10;
    xi = x*20;
    yi = y*20;
    diameter = 5;
  }
  
  public void setColor(int dim){
    if(dim > 255)
      dim = 255;
    float meanR = 0, meanG= 0, meanB = 0;
    int numPixels = width/xPanels/stride * height/yPanels/stride;
    for(int i = 0; i < width/xPanels/stride; i++){
      for(int j = 0; j < height/yPanels/stride; j++){
        colour = get(xi+i ,yi+j);
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
  
  public void draw(){
    fill(red(colour), green(colour), blue(colour));
    stroke(red(colour), green(colour), blue(colour));
    circle(x, y, diameter);
  }
  
  public String toString(){
    return("LED[" + x + "][" + y + "] with color: " + colour);
  }
}

//Global Variable Declarations
int stride = 10; //Number of LEDS in a row, we snaked our LEDs so we must specially address each led 
float widthShrink, heightShrink, aspectRatio, x=0, y=0;
int xPanels = 4, yPanels = 3, imageWidth = 40, imageHeight = 30, canvasHeight = 30, canvasWidth = 40;
color colour = color(100,100,100);
boolean initializing = true, stripsByRows = false, sendToPanels = false;
int intensity = 255;
TestObserver testObserver;
Random R = new Random();
color rain_color = color(0, 0, 127);
ArrayList<Rain> droplets;
PImage currentFrame;
int rainLength = 3;
int screenSaver = 0;
String filename = "image.jpg";
int state, r, g, b;
int circleX=0, circleY = 150, circleDirection = 1, circleIntensity = 255, circleIntensityDirection = -1, circleLegTilt = 0, circleLegTiltCounter = 0;
Boolean LEDMODE = false;
LED[][] LEDArray;

void settings() {
  String[] args = new String[]{"--num-panels-x", "4", "--num-panels-y", "3", "--screen-saver", "3", "--canvas-width", "800", "--canvas-height", "600", "--image-filename", "testing.jpg", "--led-mode", "true"};
  for(int i = 0; i < args.length; i+=1 ){ //first we should determine what the command line arguments are: 
    System.out.println(args[i]);
    if(args[i].equals("--image-width")){
      imageWidth = Integer.parseInt(args[i+1]);
    } else if(args[i].equals("--image-height")){
      imageHeight = Integer.parseInt(args[i+1]);
    } else if(args[i].equals("--num-panels-x")){
      xPanels = Integer.parseInt(args[i+1]);
    } else if(args[i].equals("--num-panels-y")){
      yPanels = Integer.parseInt(args[i+1]);
    } else if(args[i].equals("--screen-saver")){
      screenSaver = Integer.parseInt(args[i+1]);
    } else if(args[i].equals("--canvas-width")){
      canvasWidth = Integer.parseInt(args[i+1]);
    } else if(args[i].equals("--canvas-height")){
      System.out.println("old canvas height!" + canvasHeight); 
      canvasHeight = Integer.parseInt(args[i+1]);
      System.out.println("new canvas height!" + canvasHeight); 
    } else if(args[i].equals("--strips-by-rows")){
      stripsByRows = Boolean.parseBoolean(args[i+1]);
    } else if(args[i].equals("--no-panels")){
      sendToPanels = !Boolean.parseBoolean(args[i+1]);
      System.out.println("new sendToPanels!" + sendToPanels); 
    } else if(args[i].equals("--send-to-panels")){
      sendToPanels = !Boolean.parseBoolean(args[i+1]);
      System.out.println("new sendToPanels!" + sendToPanels); 
    } else if(args[i].equals("--image-filename")){
      filename = args[i+1];
    } else if(args[i].equals("--led-mode")){
      LEDMODE = Boolean.parseBoolean(args[i+1]);
    }
  }
  System.out.println(canvasWidth + "" + canvasHeight);
  size(canvasWidth, canvasHeight);
  System.out.println("CanvasWidth: " + width + " and CanvasHeight: " + height); 
}


/** Method: Function - Returns Void
* This function is responsible for preparing the program to interface with the pixelpusher.
* It specifies important values that we will use throughout the program,most of the globals are specified in this space.
*/
void setup() {
  if(screenSaver > 0 && screenSaver < 3){
    droplets = new ArrayList<Rain>(height);
    if(screenSaver == 2){
      rain_color = color(127,127,127);
      rainLength = 0;
    }
  } else if (screenSaver == 3) {
    state = 0;
    r = 255;
    g = 0;
    b = 0;
  }
  widthShrink = imageWidth/width;
  heightShrink = imageHeight/height;
  aspectRatio = width/height;
  frameRate(30); //determine the refresh rate we want the graphics to update at
  registry = new DeviceRegistry(); //create the registry 
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  registry.setFrameLimit(1);
  background(0); //initialize a black screen
  colorMode(RGB, 255, 255, 255, 255); //Specify the colormode of the pixels and their max values in RGBI mode (Red Green Blue Intensity)
  rectMode(CORNER);
  if(LEDMODE){
    LEDArray = new LED[xPanels*stride][yPanels*stride];  //initialize the array of LEDS
    for(int x = 0; x < xPanels*stride; x++){
      for(int y = 0; y < yPanels*stride; y++){
        LEDArray[x][y] = new LED(x, y);
      }
    }
  }
}

void draw() {
   if (testObserver.hasStrips || !sendToPanels) { //scrape for the strips and determine if we can send to the pixelpusher
     List<Strip> strips = registry.getStrips();
     registry.setExtraDelay(0);
     registry.startPushing();
     
     //Try to wipe the canvas completely
     stroke(0,0,0);
     fill(0,0,0);
     rect(0, 0, width, height); //Wipe the canvas and reload
     
     //THIS IS THE SECTION OF THE CODE WHICH READS IN THE IMAGE FROM THE DIRECTORY
     if(screenSaver == 0){ //standard where we load from a file
       currentFrame = loadImage(filename);
       imageMode(CORNER);
       image(currentFrame, 0,0,width, height);
     } else if(screenSaver == 1 || screenSaver == 2) { //if(screenSaver == 1){ // doing a screensaver of some time
       int newRainStart = R.nextInt(width/(width/xPanels/stride)); //get a random starting point for the new rain drop
       newRainStart = newRainStart*(width/xPanels/stride);
       Rain newRain = new Rain(newRainStart, 0);
       droplets.add(newRain);
       fill(rain_color);
       for(int i = 0; i < droplets.size(); i++){
         Rain drop = droplets.get(i);
         rect(drop.x, drop.y, drop.radius, drop.radius);
         drop.y = drop.y + drop.radius;
         //System.out.println(drop.toString());
         
         for(int j = 0; j < rainLength; j++){
           stroke(0,j*25,127-j*25);
           rect(drop.x, drop.y - j*drop.radius, drop.radius, drop.radius);
         }
         if(drop.y > height + rainLength){
           droplets.remove(i);
         }
       }
     } else if (screenSaver == 3) {
       stroke(r,g,b);
       fill(r,g,b);
       rect(0, 0, width, height); //Wipe the canvas and reload
       if(state == 0){
         g++;
         if(g==255) state = 1;
       }
       if(state == 1) {
         r--;
         if(r == 0) state = 2;
       }
       if(state == 2){
         b++;
         if(b==255) state = 3;
       }
       if(state == 3) {
         g--;
         if(g == 0) state = 4;
       }
       if(state == 4){
         r++;
         if(r==255) state = 5;
       }
       if(state == 5) {
         b--;
         if(b == 0) state = 0;
       }
     } else if (screenSaver == 4){
       //This screensaver animates a person walking from left to right and then back to left
       ///stroke(255-circleIntensity,255-circleIntensity,255-circleIntensity); //We stopped using this because we didnt want the random dimming
       //fill(255-circleIntensity,0,255-circleIntensity);
       stroke(255,255,255);
       fill(255,0,255);
       if(state == 0){
         circleLegTilt = 0;
         if(circleLegTiltCounter == 5){
           state = 1; 
           circleLegTiltCounter=0;
         }
       } else if(state == 1){
         circleLegTilt = 1;
         if(circleLegTiltCounter == 5){
           state = 2; 
           circleLegTiltCounter=0;
         }
       } else if(state == 2){
         circleLegTilt = 0;
         if(circleLegTiltCounter == 5){
           state = 3; 
           circleLegTiltCounter=0;
         }
       } else if(state == 3){
         circleLegTilt = -1;
         if(circleLegTiltCounter == 5){
           state = 0; 
           circleLegTiltCounter=0;
         }
       }
       circleLegTiltCounter++;
       
       
       if(circleX >= 800){
         circleDirection = -1;
       }
       if(circleX < 0){
         circleDirection = 1;
       }
       switch(circleLegTilt){
         case 0: //no tilts at all
           quad(circleX-70+50, circleY+200, circleX-70+50+50, circleY+200, circleX-70+50+50, circleY+200+150,  circleX-70+50, circleY+200+150); //left leg standing straight up and down
           quad(circleX+20-50, circleY+200, circleX+20+50-50, circleY+200, circleX+20+50-50, circleY+200+150, circleX+20-50, circleY+200+150); //right leg standing straight up and down
           break;
         case 1: //right leg forward
           quad(circleX-70+15+50, circleY+200-35, circleX-70+50+50, circleY+200, circleX-70+35-106+50, circleY+200+150-35,  circleX-70-106+50, circleY+200+150-70); //left leg moving to the right
           quad(circleX+20-50, circleY+200, circleX+20+50-15-50, circleY+200-35, circleX+20+35+106-50, circleY+200+150-70, circleX+20+106-50, circleY+200+150-35); //right leg moving to the left
           break;
         case -1: //
           quad(circleX-70+50, circleY+200, circleX-70+35+50, circleY+200-35, circleX-70+35+106+50, circleY+200+150-70,  circleX-70+106+50, circleY+200+150-35); //left leg goes to the right
           quad(circleX+20+15-50, circleY+200-35, circleX+20+50-50, circleY+200, circleX+20+35-106-50, circleY+200+150-35, circleX+20-106-50, circleY+200+150-70); //right leg goes to the left
           break;
       }
       triangle(circleX, circleY, circleX-50, circleY+200, circleX+50, circleY+200);
       circle(circleX,circleY,100);
       /*
    
       if(circleIntensity >254){
         circleIntensityDirection = -1;
       }
       if(circleIntensity < 2){
         circleIntensityDirection = 1;
       }
       circleIntensity += circleIntensityDirection*1;
       */
       circleX += (circleDirection * 15);
       //System.out.println("CircleIntensity is: " + circleIntensity);
     }
     
     
     //If LEDMODE is true, then we can make the display look like LEDS on our LEDWall at benedum
     if(LEDMODE){ //changes the display to look a bit more like what it would like on the  ledwall at Pitt
       //First iterate through the screen so we can get the colors for each of the pixels
       for(int x = 0; x < xPanels*stride; x++){
         for(int y = 0; y < yPanels*stride; y++){
           LED curr = LEDArray[x][y];
           curr.setColor(0);
           //System.out.println(curr.toString());
         }
       }
      fill(0,0,0);
      stroke(0,0,0);
      rect(0,0,width,height);
      //we drew the screen already so we need to wipe it and redraw the correct setup of LEDs
       for(int x = 0; x < xPanels*stride; x++){
         for(int y = 0; y < yPanels*stride; y++){
           LED curr = LEDArray[x][y];
           curr.draw();
         }
       }
     }
     
     
     //THIS IS THE SECTION OF CODE WHICH TRANSLATES THE CANVAS TO THE PHYSICAL PANEL
     // for every strip: we want to go through each LED and determine the location that LED should relate to on the canvas
     if(sendToPanels){
       int stripOffsetX, stripOffsetY, panelPixelX, panelPixelY, canvasX, canvasY;
       float r, g, b;
       for(Strip strip : strips) {
         if(stripsByRows){
           stripOffsetX = 0;
           stripOffsetY = strip.getStripNumber() * height/yPanels;
         } else {
           stripOffsetX = strip.getStripNumber()*width/xPanels;
           stripOffsetY = 0;
         }
         for (int LEDIndex = 0; LEDIndex < strip.getLength(); LEDIndex++) { // for every pixel in the physical strip
           panelPixelX = LEDIndex % stride; 
           panelPixelY = LEDIndex / stride;          
           if(panelPixelY%2 == 1){
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
           
           color newC = color(g,r,b);
           strip.setPixel(newC, LEDIndex);
        }
      }
    }
  }
}
