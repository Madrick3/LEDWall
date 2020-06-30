//Define global objects for the ball and paddles //<>//
Ball ball;
Paddle paddleLeft;
Paddle paddleRight;

public class Pong{
	public Pong(){
		ball = new Ball(width/2, height/2);
    ball.vX = 5;
    ball.vY = random(-3,3); //Spices up the game!

    paddleLeft = new Paddle(15, height/2, 30,200, 1);
    paddleRight = new Paddle(width-15, height/2, 30,200, 2);
	}
	

	//methods
	public void update(){
		ball.updateMove();
    paddleLeft.updateMove();
    paddleRight.updateMove();
    
    if ( ball.left() < paddleLeft.right() && ball.y > paddleLeft.top() && ball.y < paddleLeft.bottom()){
      ball.vX = -ball.vX;
      ball.vY = map(ball.y - paddleLeft.y, -paddleLeft.h/2, paddleLeft.h/2, -10, 10);
    }

    if ( ball.right() > paddleRight.left() && ball.y > paddleRight.top() && ball.y < paddleRight.bottom()) {
      ball.vX = -ball.vX;
      ball.vY = map(ball.y - paddleRight.y, -paddleRight.h/2, paddleRight.h/2, -10, 10);
  }
	}


	public void draw(){
		ball.draw();
    paddleLeft.draw();
    paddleRight.draw();
  }
}


// Ball object
public class Ball{
	float x, y, vX, vY, diameter;
  float speed = 10.0;

  // Constructor
	public Ball(int x, int y){
		this.x = x;
		this.y = y;
		vX = 0;
		vY = 0;
    diameter = 60.0;
	}

	public void updateMove(){
		x += vX;
		y += vY;

		if (ball.right() > width){
      ball.x = width/2;
      ball.y = height/2;
    }
    if (ball.left() < 0){
      ball.x = width/2;
      ball.y = height/2;
    }
    if (ball.bottom() > height){
      ball.vY = -ball.vY;
    }
    if (ball.top() < 0){
      ball.vY = -ball.vY;
    } 
	}

  //functions to help with collision detection
  float left(){
    return x-diameter/2;
  }
  float right(){
    return x+diameter/2;
  }
  float top(){
    return y-diameter/2;
  }
  float bottom(){
    return y+diameter/2;
  }
  
  //functions to find ball coordinates
  public float getballX(){
     return x;
  }
  
  public float getballY(){
     return y;
  }
  
  
	public void draw(){
		fill(255,255,255);
		stroke(255,0,0);
		circle(x, y, diameter);
	}
}



public class Paddle{
	float x, y, vY, w, h, speed = 3;
  int player;
  
  public Paddle(float x, float y, float w, float h, int player){
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.player = player;
    vY = speed;
  }
  
  public float getMoveY(){
    return y; 
  }
  
  public void updateMove(){
    y += vY;
    
    if (paddleLeft.bottom() > height) {
      paddleLeft.y = height-paddleLeft.h/2;
    }
  
    if (paddleLeft.top() < 0) {
      paddleLeft.y = paddleLeft.h/2;
    }
      
    if (paddleRight.bottom() > height) {
      paddleRight.y = height-paddleRight.h/2;
    }
  
    if (paddleRight.top() < 0) {
      paddleRight.y = paddleRight.h/2;
    }    
    if (ball.getballX() < width/2 && player == 1){
      ballTracker();
    }else if (ball.getballX() > width/2 && player == 2){
      ballTracker();
    }
  }
  
  public void ballTracker(){
    if(y != ball.getballY()){
        if(y-ball.getballY() < 0){
          vY = speed;
        }
        else{
          vY = -speed;
        }
      }
  }
  
  
  //helper functions
  float left(){
    return x-w/2;
  }
  float right(){
    return x+w/2;
  }
  float top(){
    return y-h/2;
  }
  float bottom(){
    return y+h/2;
  }
    
  
  public void draw() {
    fill(255,255,255);
    stroke(255,0,0);
    rectMode(CENTER);
    rect(w/2, paddleLeft.getMoveY(), w, h);
    rect(width-w/2, paddleRight.getMoveY(), w, h);
    rectMode(CORNER);
  }
}
