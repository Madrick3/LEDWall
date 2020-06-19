static public float pi = 3.14159;
static public float G = 10;
final public color[] planetColors = {color(255,0,0), color(0,255,0), color(0,0,255), color(255,0,255), color(0,128,255)};// color(#FFC081),};// color(#FF4DC1)};

public class Space{
  ArrayList<Planet> SolarSystem;
  ArrayList<star> stars;
  Planet Sun = new Planet(width/2, height/2);
  
  public Space(int numPlanets){
    SolarSystem = new ArrayList();
    for(int i = 0; i < numPlanets; i++){
      SolarSystem.add(new Planet(SolarSystem, Sun));
    }
    stars = new ArrayList();
    int numStars = 100 + (int) random(width/1600);
    for(int i = 0; i < numStars; i++)
      stars.add(new star());
  }
  
  public void update(){
    for(Planet p: SolarSystem){
      p.update();
    }
    for(int i = 0; i < SolarSystem.size(); i++){
      if(SolarSystem.get(i).skip)
        SolarSystem.remove(i);
    }
    
  }
  
  public void draw(){
    for(star s: stars){
      s.draw();
    }
    Sun.draw();
    for(Planet p: SolarSystem){
      p.draw();
    }
    
  }
  
  public class star{
    int x, y, radius, intensity;
    public star(){
      x = (int) random(width);
      y = (int) random(height);
      radius = 5 + (int) random(10);
      intensity = 128 + (int) random(128);
    }
    
    public void draw(){
      fill(intensity, intensity, intensity);
      stroke(intensity, intensity, intensity);
      circle(x,y, radius);
    }
  }
  
  public class Planet{
    PVector velocity, acceleration;
    float x, y, radius, ran;
    float mass;
    color colour;
    int colorIndex;
    ArrayList<Planet> SolarSystem;
    Planet Sun;
    Boolean skip = false;
    
    public Planet(ArrayList<Planet> SolarSystem, Planet Sun){
      x = (int) random(width);
      y = (int) random(height);
      radius = 15 + width/100*(int)random(5);
      colorIndex = (int) random(planetColors.length);
      colour = planetColors[colorIndex];
      mass = radius;
      this.SolarSystem = SolarSystem;
      this.Sun = Sun;
      
      acceleration = new PVector(0,0);
      velocity = getInitialVelocity();
    }
    
    public Planet(int x, int y){
      this.x = x;
      this.y = y;
      radius = width/16;
      colour = color(255, 255, 255);
      mass = 300;
      acceleration = new PVector(0,0);
      velocity = new PVector(0,0);
      this.Sun = this;
    }
    
    public PVector getInitialVelocity(){
      PVector distance, vi = new PVector(0,0);
      distance = new PVector(this.x-Sun.x, this.y-Sun.y);
      float vMag = sqrt(G * Sun.mass / distance.mag())*0.85;
      vi.set(-1*vMag*distance.y/distance.mag(), vMag*distance.x/distance.mag());
      return vi; 
    }
    
    public PVector partialAccel(Planet p){
      PVector acceleration, distance;
      float a;
      distance = new PVector(this.x - p.x, this.y - p.y);
      //distance = new PVector(p.x-this.x, p.y-this.y);
      if(distance.mag() < this.radius/2 || distance.mag() < p.radius/2){
        merge(p);
        
        acceleration = new PVector(0,0);
        return acceleration;
      }
      a = G*p.mass/distance.magSq();
      acceleration = new PVector(a*-1*distance.x/distance.mag(), a*-1*distance.y/distance.mag());
      return acceleration;
    }
    
    public void updateAcceleration(){
      acceleration = new PVector(0,0);
      acceleration.add(partialAccel(Sun));
      for(Planet p: SolarSystem){
        if((p != this) && !p.skip){
          acceleration.add(partialAccel(p));
        }    
      }
    }
    
    public void merge(Planet p){
      p.radius = pow(radius, 2) + pow(p.radius, 2);
      p.radius = sqrt(p.radius);
      float temp = mass;
      p.mass += mass;
      velocity.x*=mass/(mass+p.mass); velocity.y*=mass/(mass+p.mass); p.velocity.x*=mass/(mass+p.mass); p.velocity.y*=mass/(mass+p.mass);
      p.velocity.add(velocity);
      p.colour = color((red(p.colour) + red(this.colour))/2, (green(p.colour) + green(this.colour))/2, (blue(p.colour) + blue(this.colour))/2);
      skip = true;
    }
  
    public void update(){
      updateAcceleration();
      acceleration.x/=2;
      acceleration.y/=2;
      velocity.add(acceleration.x, acceleration.y);
      x = x + velocity.x/2 + acceleration.x/4; 
      y = y + velocity.y/2 + acceleration.y/4;
    }
    
    public void draw(){
      float diamond = 2*radius/3;
      stroke(255,0,0);
      line(this.x, this.y, this.x+acceleration.x*10, this.y+acceleration.y*10);
      stroke(0,255,0);
      line(this.x, this.y, this.x+velocity.x*10, this.y+velocity.y*10);
      
      stroke(255,255,255);
      fill(colour);
      rectMode(CORNERS);
      
      if(frameCount%(15+(int)random(30)) ==0)
        ran = random(pi/3) + 0.1;
      if(this.Sun == this){
        stroke(255,255,255);
        fill(red(colour)%55+200, green(colour)%55+200, blue(colour)%55+200);
        rectMode(CORNERS);
        rect(x-radius/2, y-radius/2, x+radius/2, y+radius/2);
        quad(x, y-diamond, x+diamond, y, x, y+diamond, x-diamond, y);
        quad(x+diamond*cos(ran),y+diamond*sin(ran), x+diamond*cos(ran + pi/2),y+diamond*sin(ran + pi/2), x+diamond*cos(ran + pi),y+diamond*sin(ran + pi), x+diamond*cos(ran + 3*pi/2),y+diamond*sin(ran + 3*pi/2));
      } else {
        circle(x,y,radius);
      }
    }
    
  }
  
}
