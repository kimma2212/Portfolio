import org.apache.hadoop.conf.*; 
import org.apache.hadoop.fs.*; 

public class lab1 {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub

		// creates a configuration object to configure the Hadoop system 
        Configuration conf = new Configuration();  
        
        // Get an instance of the Filesystem using configuration 
        FileSystem fs = FileSystem.get(conf); 
        
        String path_name = "/lab1/bigdata"; 
        Path path = new Path(path_name); 
        
        
        FSDataInputStream fin = fs.open(path);
        
        //System.out.println(fin);
        
        long min = 1000000000;
        long max = 1000000999;
	    
        byte[] buffer = new byte[(int)(max-min+1)];
        
        //fin.readFully(min, buffer, 0, (int)(max-min+1));
        fin.readFully(min, buffer);
       
        //8 bit xor 
        int xor = buffer[0];
        for(int i=0; i <= buffer.length-1; i++) {
        	//xor = xor ^ fin.read();
        	xor ^= buffer[i];
        }
        
        //print
        System.out.println("XOR:  " + xor);
        
        //close
        fin.close();
        fs.close();
        
	}

}
