public class Interface {

  private Socket socket = null;
  private SocketAddress address;
  private PrintWriter out;
  private BufferedReader in;
  private DataOutputStream pythonOut = null;
  private boolean socketPass = false;

  private String ip = "localhost";
  private int port = 2004;
  public Scanner sc;

  final char startChar = 's';
  final char endChar = 'e';
  final char pointChar = 'p';
  final char linechar = 'l';
  final char coordDelim = ',';
  final char ready = 'q';  


  public Interface() {
    try {
      address = new InetSocketAddress(ip, port);
      socket = new Socket();
      socket.connect(address);
      println("Processing Connected to a socket");
      //drawDebugMessage("Connected to socket", 2);
      //drawDebugMessage(socket.toString(), 3);
      out = new PrintWriter(socket.getOutputStream(), true);
      in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
      socketPass = true;
    } 
    catch(Exception e) {
      println(e); 
      socketPass = false;
    };
  }


  /*
  public Interface(){
   sc = new Scanner(System.in);
   }
   
   public void readNext(){
   if(sc.hasNext()){
   String text = sc.next();
   println(text);
   drawDebugMessage(text, 9);
   } else {
   drawDebugMessage("No Message", 8);
   }
   }
   */

  /** Blocking function
   * Socket will read in from terminal and check for 'S'
   * After receiving 'S', Socket will process incoming messages until an 'E' message is received
   *
   */
  public void readMessageAndDraw() {
    //drawDebugMessage("starting read\n", 6);
    boolean keepGoing = true, start = false;
    String raw;
    String [] split;
    int [] coords;
    ArrayList<drawing> drawings = new ArrayList<drawing>();
    try {
      fill(255, 255, 255);
      textSize(32);
      println("starting readline");
      raw = in.readLine(); 
      println(raw);
      if (!raw.isEmpty()) {
        if (raw.equals("S")) {
          println("S Found, Start initialized");
          start = true;
        } else {
          start = false;
        }
      }
      while (start) {
        raw = in.readLine();
        println(raw);
        if (!raw.isEmpty()) {
          split = split(raw, ":");
          println("Split: ", split);
          if (split[0].equals("E")) {
            start = false;
          } else if (split[0].equals("P")) {
            println("creating point");
            coords = int(split(split[1], " "));
            drawings.add(new drawing(1, coords[0], coords[1]));
          } else if (split[0].equals("R")) {
            println("creating rectangle");
            coords = int(split(split[1], " "));
            drawings.add(new drawing(2, coords[0], coords[1]));
          }
        }
        for (drawing d : drawings) {
          d.draw();
        }
      } 
    }catch(Exception e) {
        fill(255, 255, 255);
        println("Something went wrong");
        textSize(32);
        text("ERROR: INTERFACE TRYCATCH ERROR", 0, 64);
        text(e.toString(), 0, 96);
      }
    }


    public void sendReady() {
      //drawDebugMessage("ready called", 7);
      try {
        out.write("*");
      } 
      catch(Exception e) {
        print("Something went wrong with send");
      }
    }
  }
