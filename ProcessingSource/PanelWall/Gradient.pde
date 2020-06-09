
public class Gradient {
  int r=255, g=0, b=0, colorState=0, step;

  public Gradient(int step) {
    this.step = step;
  }

  public void draw() {
    clearCanvas();
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
