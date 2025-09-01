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
public class Ex2 {
        
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
        //counts.addSink(new sinkFunction());
        
        
        counts.print();
        
 
         env.execute("Streaming WordCount Example");
    }  
   
    

    public static final class Tokenizer implements FlatMapFunction<String, Tuple2<String, Integer>> {

        public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
            // normalize and split the line
            String[] tokens = value.toLowerCase().split("\\W+");

            
            
            // emit the pairs
            for (int i = 0; i < tokens.length - 1; i++) {
                if (tokens[i].length() > 0 && tokens[i + 1].length() > 0) {
                    out.collect(new Tuple2<String, Integer>(tokens[i] + " " + tokens[i + 1], 1));
                }
            }
        }
    }
}