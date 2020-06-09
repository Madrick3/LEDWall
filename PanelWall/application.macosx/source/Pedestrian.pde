public class Pedestrian{
  int state;
  int circleX=0, circleY = 150; 
  int circleDirection = 1, circleIntensity = 255, circleIntensityDirection = -1;
  int circleLegTilt = 0, circleLegTiltCounter = 0; //walker screensaver
  
  public Pedestrian(){
    state = 0;
  }
  
  public void draw(){
    //This screensaver animates a person walking from left to right and then back to left
      ///stroke(255-circleIntensity,255-circleIntensity,255-circleIntensity); //We stopped using this because we didnt want the random dimming
      //fill(255-circleIntensity,0,255-circleIntensity);
      stroke(255, 255, 255);
      fill(255, 0, 255);
      if (state == 0) {
        circleLegTilt = 0;
        if (circleLegTiltCounter == 5) {
          state = 1; 
          circleLegTiltCounter=0;
        }
      } else if (state == 1) {
        circleLegTilt = 1;
        if (circleLegTiltCounter == 5) {
          state = 2; 
          circleLegTiltCounter=0;
        }
      } else if (state == 2) {
        circleLegTilt = 0;
        if (circleLegTiltCounter == 5) {
          state = 3; 
          circleLegTiltCounter=0;
        }
      } else if (state == 3) {
        circleLegTilt = -1;
        if (circleLegTiltCounter == 5) {
          state = 0; 
          circleLegTiltCounter=0;
        }
      }
      circleLegTiltCounter++;


      if (circleX >= 800) {
        circleDirection = -1;
      }
      if (circleX < 0) {
        circleDirection = 1;
      }
      switch(circleLegTilt) {
      case 0: //no tilts at all
        quad(circleX-70+50, circleY+200, circleX-70+50+50, circleY+200, circleX-70+50+50, circleY+200+150, circleX-70+50, circleY+200+150); //left leg standing straight up and down
        quad(circleX+20-50, circleY+200, circleX+20+50-50, circleY+200, circleX+20+50-50, circleY+200+150, circleX+20-50, circleY+200+150); //right leg standing straight up and down
        break;
      case 1: //right leg forward
        quad(circleX-70+15+50, circleY+200-35, circleX-70+50+50, circleY+200, circleX-70+35-106+50, circleY+200+150-35, circleX-70-106+50, circleY+200+150-70); //left leg moving to the right
        quad(circleX+20-50, circleY+200, circleX+20+50-15-50, circleY+200-35, circleX+20+35+106-50, circleY+200+150-70, circleX+20+106-50, circleY+200+150-35); //right leg moving to the left
        break;
      case -1: //
        quad(circleX-70+50, circleY+200, circleX-70+35+50, circleY+200-35, circleX-70+35+106+50, circleY+200+150-70, circleX-70+106+50, circleY+200+150-35); //left leg goes to the right
        quad(circleX+20+15-50, circleY+200-35, circleX+20+50-50, circleY+200, circleX+20+35-106-50, circleY+200+150-35, circleX+20-106-50, circleY+200+150-70); //right leg goes to the left
        break;
      }
      triangle(circleX, circleY, circleX-50, circleY+200, circleX+50, circleY+200);
      circle(circleX, circleY, 100);
      circleX += (circleDirection * 15);
  }
}
