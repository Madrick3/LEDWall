public class PixelPusher {

  DeviceRegistry registry;   
  TestObserver testObserver;
  List<Strip> strips;

  public PixelPusher() {
    registry = new DeviceRegistry(); //create the registry 
    testObserver = new TestObserver();
    registry.addObserver(testObserver);
    registry.setFrameLimit(1);
  }

  public void drawSetup() {
    strips = registry.getStrips();
    registry.setExtraDelay(0);
    registry.startPushing();
  }

  public boolean canSendToStrips() {
    return(testObserver.hasStrips);
  }

  public void pushToPixelPusher() {
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

private class TestObserver implements Observer { //This observer class verifies that a pixelpusher is connected to the raspberry pi through the network switch, it also gives us an easy way to connect to and interface with the pixelpusher
  public boolean hasStrips = false;
  public void update(Observable registry, Object updatedDevice) {
    println("Registry changed!");
    if (updatedDevice != null) {
      println("Device change: " + updatedDevice);
    }
    this.hasStrips = true;
  }
};
