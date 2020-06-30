public class Bouncy{
  PVector location;  // Location of the ball in the x,y grid
  PVector velocity;  // Velocity of the ball in the x,y grid
  PVector gravity;   // Gravity acts like gravity on the ball
  float diameter, radius; // Diameter and radius of the ball
  //int r,g,b;
  
  public Bouncy(){
    location = new PVector(100,100); // Starting location of the ball, can be adjusted
    velocity = new PVector(3, 2.6); // Initial horizontal and vertical velocities (x, y)
    gravity = new PVector(0,0.4); // While gravity is acceleration, for now it is velocity
    diameter = 74.0; // Diameter of ball, can be adjusted
    radius = diameter/2; // Radius is half the diameter
  }
  
  public void update(){
    // Add velocity to the location, thus moving the ball.
    location.add(velocity);
    
    // Add gravity to velocity, thus reducing or increasing the speed of the ball
    // depending on the direction of the balls vertical velocity
    velocity.add(gravity);
    
    // Bounces the ball of the screen edges
    if ((location.x > width - radius) || (location.x < radius)) {
      velocity.x = velocity.x * -1; // Reverses the balls horizontal direction
    }
    
    if (location.y > height-radius) {
      // We're reducing velocity ever so slightly 
      // when it hits the bottom of the window
      velocity.y = velocity.y * -0.95; 
      location.y = height-radius; // Keeps the ball above ground
    }
    
    // If the cursor is over the ball, change the position
    if (abs(mouseX - location.x) < radius && abs(mouseY - location.y) < radius) {
      velocity.sub(gravity);
      
      //location.x += random(-20, 20);
      //location.y += random(-20, 20);
    }
    
  }
  
  public void draw() {
  background(0); // Sets the background color to black
  stroke(255); // Sets the outline of the ball to be white
  strokeWeight(2); // Sets the width of the outline
  fill(255,255,255); // Fills in the outline shape with white
  circle(location.x,location.y, diameter); // Creates the shape as a circle at location coordinates
  }
  /*
  if (abs(mouseX - location.x) < radius && abs(mouseY - location.y) < radius) {
    if(r>80){
      r -= 4;
      ballDraw(r,0,0);
    }
    else if (g>80){
      g -= 4;
      ballDraw(0,g,0);
    }
    else if (b>80){
      b -= 4;
      ballDraw(0,0,b);
    } 
    else {
      r=g=b=255;
      ballDraw(r,g,b);
    }
  }
  else {
    ballDraw(r,g,b);
  }
  
  ballDraw(0,255,0);
  }
  
  public void ballDraw(int rr,int gg,int bb){
  // Display circle at location vector
    stroke(255);
    strokeWeight(2);
    fill(rr,gg,bb);
    circle(location.x,location.y, diameter);
  }
  */
}
