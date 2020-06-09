public class Drawing {
  int t;
  int[] x, y;
  int special;
  String message;
  color colour = color(255, 0, 255);

  public Drawing(int t, int[] x, int[] y) {
    this.t = t;
    this.x = new int[x.length];
    this.y = new int[y.length];
    for (int i = 0; i < x.length; i++) {
      println("in for loop for drawing: ", i);
      this.x[i] = x[i];
      this.y[i] = y[i];
    }
  }

  public Drawing(int t, int x, int y) {
    this.t = t;
    this.x = new int[t];
    this.y = new int[t];
    this.x[0] = x;
    this.y[0] = y;
  }

  public Drawing(int t, int x, int y, int s) {
    this.t = t;
    this.x = new int[t];
    this.y = new int[t];
    this.x[0] = x;
    this.y[0] = y;
    this.special = s;
  }

  public Drawing(int t, int x, int y, int s, String message) {
    this.t = t;
    this.x = new int[t];
    this.y = new int[t];
    this.x[0] = x;
    this.y[0] = y;
    this.special = s;
    this.message = message;
  }

  public void draw() {
    stroke(255, 255, 255);
    fill(colour);
    if (t == 1) {
      circle(x[0], y[0], 5);
    } else if (t == 2) {
      circle(x[0], y[0], 5);
      circle(x[1], y[1], 5);
      line(x[0], y[0], x[1], y[1]);
    } else if (t == 3) {
      circle(x[0], y[0], special);
    } else if (t == 4) {
      rectMode(CORNERS);
      rect(x[0], y[0], x[1], y[1]);
    } else if (t == 5) {
      textSize(special);
      text(message, x[0], y[0]);
    } else if (t == 6) {
      ellipse(x[0], y[0], x[1], y[1]);
    }
  }
}
