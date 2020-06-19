public class Rain {
  int rainLength = 3, newRainStart;
  ArrayList<drop> droplets;
  color rain_color = color(0, 128, 255);

  public Rain(int rainLength, color rain_color) {
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

  public void draw(color colour) {
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
