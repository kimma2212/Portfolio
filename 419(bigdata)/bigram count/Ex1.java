import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.flink.api.common.functions.FlatMapFunction;

import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.util.Collector;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

@SuppressWarnings("serial")
public class Ex1 {
        
    public static void main(String[] args) throws Exception {

        final ParameterTool params = ParameterTool.fromArgs(args);

        // set up the execution environment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // make parameters available in the web interface
        env.getConfig().setGlobalJobParameters(params);

        // get input data
        // <PATH_TO_DATA>: The path to input data, e.g., "/home/cpre419/Downloads/shakespeare"
        DataStream<String> text = env.readTextFile("/home/cpre419/Downloads/shakespeare");

        DataStream<Tuple2<String, Integer>> counts =
              // split up the lines in pairs (2-tuples) containing: (word,1)
              text.flatMap(new Tokenizer())
              // group by the tuple field "0" and sum up tuple field "1"
              .keyBy(0)
              .sum(1);

         // emit result
         //counts.print();     
        
        //Adds the given sink to the DataSteam.
        counts.addSink(new sinkFunction());
        
        
 
         env.execute("Streaming WordCount Example");
    }  
    

    
    
    //comparator for sorting
    public static class WordFrequencyComparator implements Comparator<Map.Entry<String, Integer>> {
        public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
            return o2.getValue().compareTo(o1.getValue());
        }
    }

    //sink function for word count 
    public static final class sinkFunction extends RichSinkFunction<Tuple2<String, Integer>> {
    	
    	
        // HashMap to store. word frequency
        private HashMap<String, Integer> wordCounts = new HashMap<String, Integer>();

        // Update the HashMap 
        public void invoke(Tuple2<String, Integer> value, Context context) {
            wordCounts.put(value.f0, value.f1);
        }

        // Print
        @Override
        public void close() throws IOException {
            System.out.println("Top 10");

            // Create a list from the HashMap entries
            List<Map.Entry<String, Integer>> wordList = new ArrayList<Entry<String, Integer>>(wordCounts.entrySet());

            // Sort the list by frequency in descending order using the custom comparator
            Collections.sort(wordList, new WordFrequencyComparator());

            // Print the top 10 most frequent words
            for (int i = 0; i < Math.min(10, wordList.size()); i++) {
                Map.Entry<String, Integer> entry = wordList.get(i);
                System.out.println(entry.getKey() + ": " + entry.getValue());
            }
            
            System.out.println("===============================");
            
        }
    }
    
    

    public static final class Tokenizer implements FlatMapFunction<String, Tuple2<String, Integer>> {

        public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
            // normalize and split the line
            String[] tokens = value.toLowerCase().split("\\W+");

            // emit the pairs
            for (String token : tokens) {
                if (token.length() > 0) {
                    out.collect(new Tuple2<String, Integer>(token, 1));
                }
            }
        }
    }

}