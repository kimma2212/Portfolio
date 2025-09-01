
		/**
		 * 
		 *   Experiment 2
		 *   Data: patents_small.txt
		 *   
		 *   Write a program that calculate total number of all undirected cycles of length 3 in a graph.
		 * 
		 */
		

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.PairFlatMapFunction;

import scala.Tuple2;
	


public class CycleCount {
	
	private final static int numOfReducers = 2;

	@SuppressWarnings("serial")
	public static void main(String[] args) throws Exception {
		SparkConf sparkConf = new SparkConf().setAppName("Cycle Count");
		JavaSparkContext context = new JavaSparkContext(sparkConf);
		JavaRDD<String> input = context.textFile(args[0]);


		/**
		 * 
		 *   Experiment 2
		 *   Data: patents_small.txt
		 *   
		 *   Write a program that calculate total number of all undirected cycles of length 3 in a graph.
		 * 
		 */
		


		JavaRDD<String> graphData = input.flatMap(new FlatMapFunction<String, String>() {
			public Iterator<String> call(String s) {
				return Arrays.asList(s.split("\n+")).iterator();
			}
		}).filter(f -> !f.isEmpty());

		JavaPairRDD<Long, Long> edgeData = graphData.flatMapToPair(new PairFlatMapFunction<String, Long, Long>() {
			public Iterator<Tuple2<Long, Long>> call(String s) {
				String[] t = s.split("\\s+");
				List<Tuple2<Long, Long>> res = new ArrayList<Tuple2<Long, Long>>();
				res.add(new Tuple2<Long, Long>(Long.parseLong(t[0]), Long.parseLong(t[1])));
				res.add(new Tuple2<Long, Long>(Long.parseLong(t[1]), Long.parseLong(t[0])));
				return res.iterator();
			}
		});

		JavaPairRDD<Long, ArrayList<Long>> adjList = edgeData.groupByKey().mapToPair(f -> {
			ArrayList<Long> l = new ArrayList<Long>();
			f._2().forEach(l::add);
			return new Tuple2<Long, ArrayList<Long>>(f._1(), l);
		});

JavaPairRDD<Long, Tuple2<Long, Long>> triangleCandidates = adjList.flatMapToPair(new PairFlatMapFunction<Tuple2<Long, ArrayList<Long>>, Long, Tuple2<Long, Long>>() {
	public Iterator<Tuple2<Long, Tuple2<Long, Long>>> call(Tuple2<Long, ArrayList<Long>> node) {
		Long u = node._1();
		ArrayList<Long> nbrs = node._2();
		List<Tuple2<Long, Tuple2<Long, Long>>> res = new ArrayList<Tuple2<Long, Tuple2<Long, Long>>>();

		for (Long v : nbrs) {
			if (u < v) {
				res.add(new Tuple2<Long, Tuple2<Long, Long>>(v, new Tuple2<Long, Long>(u, u)));
			}
		}

		return res.iterator();
	}
});

JavaPairRDD<Long, HashSet<Long>> groupedCandidates = triangleCandidates.groupByKey().mapToPair(f -> {
	HashSet<Long> set = new HashSet<Long>();
	f._2().forEach(t -> set.add(t._2()));
	return new Tuple2<Long, HashSet<Long>>(f._1(), set);
});

JavaPairRDD<Long, Long> triangleEdges = groupedCandidates.flatMapToPair(new PairFlatMapFunction<Tuple2<Long, HashSet<Long>>, Long, Long>() {
	public Iterator<Tuple2<Long, Long>> call(Tuple2<Long, HashSet<Long>> node) {
		Long u = node._1();
		HashSet<Long> nbrs = node._2();
		List<Tuple2<Long, Long>> res = new ArrayList<Tuple2<Long, Long>>();

		for (Long v : nbrs) {
			if (u < v) {
				res.add(new Tuple2<Long, Long>(v, u));
			}
		}

		return res.iterator();
	}
});
		JavaPairRDD<Tuple2<Long, Long>, Integer> triangleCount = triangleEdges.mapToPair(triangle -> new Tuple2<Tuple2<Long, Long>, Integer>(triangle, 1));
		long totalTriangles = triangleCount.reduceByKey((x, y) -> x + y).count();

		// Save the total number of triangles to the output file
		ArrayList<Long> triangleCountList = new ArrayList<Long>();
		triangleCountList.add(totalTriangles);
		JavaRDD<Long> triangleCountRDD = context.parallelize(triangleCountList);
		triangleCountRDD.saveAsTextFile(args[1]);

		context.stop();
		context.close();
	}
}