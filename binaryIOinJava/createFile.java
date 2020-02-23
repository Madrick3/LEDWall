/*
Author: Jackie Yang
Project: LED wall 2 XProject
Purpose: Create a file with byte stream as an input for pixel pusher
Source: https://www.geeksforgeeks.org/convert-byte-array-to-file-using-java/
*/


// Java Program to convert
// byte array to file
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;

public class createFile {

    // Path of a file
    static String FILEPATH = "pixelTest";
    static File file = new File(FILEPATH);

    // Method which write the bytes into a file
    static void writeByte(byte[] bytes)
    {
        try {

            // Initialize a pointer
            // in file using OutputStream
            OutputStream
                os
                = new FileOutputStream(file);

            // Starts writing the bytes in it
            os.write(bytes);
            System.out.println("Successfully"
                               + " byte inserted");

            // Close the file
            os.close();
        }

        catch (Exception e) {
            System.out.println("Exception: " + e);
        }
    }

    // Driver Code
    public static void main(String args[])
    {

        Integer temp = new Integer(0);

        // Get byte array from string
        byte[] bytes = new byte[3602];

        // Convert byte array to file
        temp = 30;
        bytes[0] = temp.byteValue();
        temp = 40;
        bytes[1] = temp.byteValue();
        for (int i = 2;i<3602;i=i+3)
        {
          temp = 255;
          bytes[i] = temp.byteValue();
          temp = 0;
          bytes[i+1] = temp.byteValue();
          bytes[i+2] = temp.byteValue();
        }
        writeByte(bytes);
    }
}
