public class Interface {
  public Socket socket = null;
  public PrintWriter out;
  public BufferedReader in;
  public DataOutputStream pythonOut = null;
  public boolean socketPass = false;

  final char startChar = 's';
  final char endChar = 'e';
  final char pointChar = 'p';
  final char linechar = 'l';
  final char coordDelim = ',';
  final char ready = 'q';  

  public Interface() {
    try {
      socket = new Socket("localhost", 2004);
      out = new PrintWriter(socket.getOutputStream(), true);
      in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
      socketPass = true;
    } 
    catch(Exception e) {
      println(e); 
      socketPass = false;
    };
  }

  public void readMessageAndDraw(){
    boolean keepGoing = true, start = false;
    char readin;
    String raw;
    ArrayList<Integer> x;
    ArrayList<Integer> y;
    try {
      while (keepGoing) {
        raw = in.readLine();  
        x = new ArrayList<Integer>();
        y = new ArrayList<Integer>();
        if (raw == "E") {
          start = false;
          continue;
        }
        if (raw == "S") {
          start = true;
        }
        if (raw == "P") {
          int type = 1;
          x.add(Integer.parseInt(in.readLine()));
          y.add(Integer.parseInt(in.readLine()));
          new drawing(1, x.toArray(new Integer[x.size()]), y.toArray(new Integer[y.size()]));
        }
        if (raw == "L") {
          int type = 2;
          x.add(Integer.parseInt(in.readLine()));
          y.add(Integer.parseInt(in.readLine()));
          x.add(Integer.parseInt(in.readLine()));
          y.add(Integer.parseInt(in.readLine()));
          new drawing(1, x.toArray(new Integer[x.size()]), y.toArray(new Integer[y.size()]));
        }
      }
    }  
    catch(Exception e) {
      print("Something went wrong");
    }
  }
  
  public void sendReady(){
    try{
      out.write("*");  
    } catch(Exception e){
      print("Something went wrong with send");
    }
  }
}
