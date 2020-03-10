import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import java.util.*;
import processing.core.*;


DeviceRegistry registry;


import java.io.*;
import java.net.*;

class JavaSocket {
  Socket socket;
  DataInputStream din;
  int x = 0;
  int y = 0;
  
  public JavaSocket() {
    try{
      socket = new Socket("localhost", 2004);
      din = new DataInputStream(socket.getInputStream());
      System.out.println("Socket created and datainputstream");
    } catch (IOException e){
      System.out.println("JavaSocket Error: Creating and Connecting to Socket Failed");
    }
  }
  
  public color getInput(){
    try{
      String tmp; 
      while ((tmp = din.readLine()) != null) {
          System.out.println("tmp: " + tmp);
          String[] values = tmp.split(",");
          color retThis = color(Integer.parseInt(values[0]), Integer.parseInt(values[1]), Integer.parseInt(values[2]));
          return retThis;
      }
    } catch(IOException e){
      System.out.println("IOException when retrieving input: " + e.toString());
      return(color(255,0,0));
    }
    return(color(0,255,0));
  }
  
  public color getWhiteScreen(){
    return(color(255,255,255));
  }
}


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

//Global Variable Declarations
int stride = 10; //Number of LEDS in a row, we snaked our LEDs so we must specially address each led 
float widthShrink, heightShrink, aspectRatio, x=0, y=0;
int xPanels = 4, yPanels = 3, imageWidth = 40, imageHeight = 30, canvasHeight = 30, canvasWidth = 40;
color colour = color(100,100,100);
boolean initializing = true, stripsByRows = false, sendToPanels = true;
int intensity = 255;
TestObserver testObserver;
Random R = new Random();
color rain_color = color(0, 0, 127);
ArrayList<Rain> droplets;
String newInput;
int rainLength = 3;
int screenSaver = 0;
String filename = "image.jpg";
int state, r, g, b;
int updateMode = 0; //0 == full screen replacement, 1 == changes
JavaSocket connection;

void settings() {
  //String[] args = new String[]{"--no-panels", "true", "--image-width", "400", "--image-height", "300", "--num-panels-x", "1", "--num-panels-y", "1", "--screen-saver", "0", "--canvas-width", "800", "--canvas-height", "800", "--image-filename", "testing.jpg"};
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
      canvasHeight = Integer.parseInt(args[i+1]);
    } else if(args[i].equals("--strips-by-rows")){
      stripsByRows = Boolean.parseBoolean(args[i+1]);
    } else if(args[i].equals("--no-panels")){
      sendToPanels = !Boolean.parseBoolean(args[i+1]);
    } else if(args[i].equals("--image-filename")){
      filename = args[i+1];
    }
  }
  size(canvasWidth, canvasHeight);
  System.out.println("CanvasWidth: " + width + " and CanvasHeight: " + height); 
}


/** Method: Function - Returns Void
* This function is responsible for preparing the program to interface with the pixelpusher.
* It specifies important values that we will use throughout the program,most of the globals are specified in this space.
*/
void setup() {
  if(screenSaver == 0){
    connection = new JavaSocket();
  } else if (screenSaver > 0 && screenSaver < 3){
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
       if(updateMode == 0){
         System.out.println("requesting input - full screen");
         color inputPixel;
         for(int row = 0; row < width; row++){
           System.out.println("new row");
           for(int col = 0; col < height; col++){
             inputPixel = connection.getInput();
             stroke(red(inputPixel), green(inputPixel), blue(inputPixel));
             fill(red(inputPixel), green(inputPixel), blue(inputPixel));
             point(col,row);
           }
         }
       } else {
         System.out.println("this is not yet implemented");
       }
     } else if(screenSaver == 1 || screenSaver == 2) {
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
     }  
     
     //THIS IS THE SECTION OF CODE WHICH TRANSLATES THE CANVAS TO THE PHYSICAL PANEL
     // for every strip: we want to go through each LED and determine the location that LED should relate to on the canvas
     if(sendToPanels){
       //System.out.println("sending to panels");
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
         
         
         
         
         
         
         
         
