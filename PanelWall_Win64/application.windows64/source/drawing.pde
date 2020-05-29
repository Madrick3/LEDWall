public class drawing {
  int type;
  int[] x, y;
  color colour = color(255, 0, 255);
  
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
