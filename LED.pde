//Declares the class that is the screen saver
public class LED {
  //Declares the variables being used
  public int x, y, xi, yi, diameter, intensity;
  public color colour;
  
  //Class constructor, initializes the start values of the variables
  //every time the class is called
  public LED(int x, int y) { //requires two int values
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
