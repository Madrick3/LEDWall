public class drawing {
  int t;
  int[] x, y;
  color colour = color(255, 0, 255);
  
  public drawing(int t, int[] x, int[] y) {
    this.t = t;
    this.x = new int[t];
    this.y = new int[t];
    for(int i = 0; i < t; i++){
      this.x[i] = x[i];
      this.y[i] = y[i];
    }
  }
  
  public drawing(int t, int x, int y) {
    this.t = t;
    this.x = new int[t];
    this.y = new int[t];
    this.x[0] = x;
    this.y[0] = y;
  }
  
  public void draw(){
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
