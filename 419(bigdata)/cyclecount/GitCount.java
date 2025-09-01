import java.util.Arrays;
import java.util.Iterator;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFunction;

import scala.Tuple2;

public class GitCount {

	private final static int numOfReducers = 2;

	@SuppressWarnings("serial")
	public static void main(String[] args) throws Exception {
		
		if (args.length != 2) {
			System.err.println("Usage: GitCount <language> <num_of_repo> <name_of_repo_highest_start> <num_stars>");
			System.exit(1);
		}

		SparkConf sparkConf = new SparkConf().setAppName("GitCount in Spark");
				//.setMaster("local[*]");
		JavaSparkContext context = new JavaSparkContext(sparkConf);
		JavaRDD<String> lines = context.textFile(args[0]);
		
		
		/**
		 * 
		 *   Experiment 1
		 *   Data: "github.csv
		 *   For each language,
		 *   	1) Find out how many repositories using it;
		 *   	2) One repository that has highest number using it.
		 *   format: <language> <num_of_repo> <name_of_repo_highest_start> <num_stars>
		 *   The list should be sorted by the num_of_repo in descending order.
		 * 
		 */
		
		
		//map
		//String String     language     |     count(1) repository stars 
		JavaPairRDD<String, String> language_pair = lines.mapToPair(new PairFunction<String, String, String>() {

		public Tuple2<String, String> call(String in) {

			String[] parts = in.split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)", -1);

			// Second column -> Code language <language>
			String language = parts[1];

			// First column -> repository name <name_of_repo>
			String repository = parts[0];

			// 13th Column -> stars <num_stars>
			String stars = parts[12];

			return new Tuple2<String, String>(language, "1" + " " + repository + " " + stars);
		}
	});

		
		
		
		//reduce
		//need to return 
		JavaPairRDD<String, String> counts = language_pair.reduceByKey(new Function2<String, String, String>() {
		public String call(String s1, String s2) {
			String[] part1 = s1.split(" ");
			String[] part2 = s2.split(" ");

			int count = Integer.parseInt(part1[0]) + Integer.parseInt(part2[0]);

			// Count stars to compare
			int stars1 = Integer.parseInt(part1[2]);
			int stars2 = Integer.parseInt(part2[2]);
			String topStars = stars1 > stars2 ? part1[1] + " " + stars1 : part2[1] + " " + stars2;

			return count + " " + topStars;
		}
	}, numOfReducers);
		
		
		
		
		//Part for organization.
		
		JavaPairRDD<Integer, String> swap = counts.mapToPair(new PairFunction<Tuple2<String, String>, Integer, String>(){
			public Tuple2<Integer, String> call(Tuple2<String, String> tuple){
				
				String[] token = tuple._2.split(" ");
				int num_of_repo = Integer.parseInt(token[0]);
				//return new Tuple2<Integer, String>(num_of_repo, tuple._1 + " " + tuple._2);
				return new Tuple2<Integer, String>(num_of_repo, tuple._1 + " " + token[0] + " " + token[1]+ " " + token[2]);
			}
		});
				
				
				
		JavaPairRDD<Integer, String> sorted = swap.sortByKey(false);
		
		//
		JavaRDD<String> finalOutput = sorted.map(tuple -> tuple._2);
				
		

		//sorted.saveAsTextFile(args[1]);
		finalOutput.saveAsTextFile(args[1]);
		context.stop();
		context.close();
		
	}

}