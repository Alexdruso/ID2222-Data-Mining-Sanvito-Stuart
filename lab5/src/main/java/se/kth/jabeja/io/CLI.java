package se.kth.jabeja.io;

import org.apache.log4j.Logger;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;
import se.kth.jabeja.annealing.AnnealingType;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.GraphInitColorPolicy;
import se.kth.jabeja.config.NodeSelectionPolicy;

import java.io.File;
import java.io.FileNotFoundException;

/**
 * Created by salman on 10/25/16.
 */
public class CLI {
  final static Logger logger = Logger.getLogger(CLI.class);

  @Option(name = "-help", usage = "Print usages.")
  private boolean HELP = false;

  @Option(name = "-rounds", usage = "Number of rounds.")
  private int ROUNDS = 1000;

  @Option(name = "-numPartitions", usage = "Number of partitions.")
  private int NUM_PARTITIONS = 4;

  @Option(name = "-uniformRandSampleSize", usage = "Uniform random sample size.")
  private int UNIFORM_RAND_SAMPLE_SIZE = 6;

  @Option(name = "-temp", usage = "Simulated annealing temperature.")
  private float TEMPERATURE = 2;

  @Option(name = "-delta", usage = "Simulated annealing delta.")
  private float DELTA = (float) 0.003;

  @Option(name = "-seed", usage = "Seed.")
  private int SEED = 0;

  @Option(name = "-alpha", usage = "Alpha parameter")
  private float ALPHA = 2;

  @Option(name = "-randNeighborsSampleSize", usage = "Number of random neighbors sample size.")
  private int randNeighborsSampleSize = 3;

  @Option(name = "-graphInitColorSelectionPolicy", usage = "Initial color celection policy. Supported, RANDOM, ROUND_ROBIN, BATCH")
  private String GRAPH_INIT_COLOR_SELECTION_POLICY = "ROUND_ROBIN";
  private GraphInitColorPolicy graphInitColorSelectionPolicy = GraphInitColorPolicy.ROUND_ROBIN;

  @Option(name = "-nodeSelectionPolicy", usage = "Node selection plicy. Supported, RANDOM, LOCAL, HYBRID")
  private String NODE_SELECTION_POLICY = "HYBRID";
  private NodeSelectionPolicy nodeSelectionPolicy = NodeSelectionPolicy.HYBRID;

  @Option(name = "-graph", usage = "Location of the input graph.")
  private static String GRAPH = "./graphs/ws-250.graph";

  @Option(name = "-outputDir", usage = "Location of the output file(s)")
  private static String OUTPUT_DIR = "./output";

  @Option(name="-annealingType", usage = "Sets the annealing type. Support LINEAR and EXPONENTIAL")
  private static String ANNEALING_TYPE = "LINEAR";
  private AnnealingType annealingType = AnnealingType.LINEAR;

  public Config parseArgs(String[] args) throws FileNotFoundException {
    CmdLineParser parser = new CmdLineParser(this);
    parser.setUsageWidth(80);
    try {
      // parse the arguments.
      parser.parseArgument(args);

      graphInitColorSelectionPolicy = GraphInitColorPolicy.valueOf(GRAPH_INIT_COLOR_SELECTION_POLICY.toUpperCase());
      nodeSelectionPolicy = NodeSelectionPolicy.valueOf(NODE_SELECTION_POLICY.toUpperCase());
      annealingType = AnnealingType.valueOf(ANNEALING_TYPE.toUpperCase());

    } catch (Exception e) {
      logger.error(e.getMessage());
      parser.printUsage(System.err);
      System.exit(-1);
    }

    File graphFile = new File(GRAPH);
    if (!graphFile.exists() || !graphFile.isFile()) {
      throw new FileNotFoundException("Graph file does not exist.");
    }

    if (HELP) {
      parser.printUsage(System.out);
      System.exit(0);
    }

    return new Config().setRandNeighborsSampleSize(randNeighborsSampleSize)
            .setDelta(DELTA)
            .setNumPartitions(NUM_PARTITIONS)
            .setUniformRandSampleSize(UNIFORM_RAND_SAMPLE_SIZE)
            .setRounds(ROUNDS)
            .setSeed(SEED)
            .setTemperature(TEMPERATURE)
            .setGraphFilePath(GRAPH)
            .setNodeSelectionPolicy(nodeSelectionPolicy)
            .setGraphInitialColorPolicy(graphInitColorSelectionPolicy)
            .setOutputDir(OUTPUT_DIR)
            .setAlpha(ALPHA)
            .setAnnealingType(annealingType);
  }
}
