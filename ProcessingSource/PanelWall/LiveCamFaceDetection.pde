import gab.opencv.*;
import processing.video.*;
import java.awt.*;

public class LiveCamFaceDetection {
  Capture video;
  OpenCV opencv;
  PApplet thisParent;
  
  public LiveCamFaceDetection(PApplet p){
    this.thisParent = p;
    video = new Capture(p, 640/2, 480/2);
    opencv = new OpenCV(p, 640/2, 480/2);
    opencv.loadCascade(OpenCV.CASCADE_FRONTALFACE);  
  
    video.start();
  }
  
  public void draw() {
  scale(2);
  opencv.loadImage(video);

  image(video, 0, 0 );
  Rectangle[] faces = opencv.detect();
  
  println(faces.length);
  
  stroke(0, 0, 0);
  fill(0, 0, 0);
  rect(0, 0, width, height); //Wipe the canvas and reload
  
  stroke(0, 255, 0);
  strokeWeight(3);
  
    for (int i = 0; i < faces.length; i++) {
      println(faces[i].x + "," + faces[i].y);
      rect(faces[i].x, faces[i].y, faces[i].width, faces[i].height);
    }
  }
}
