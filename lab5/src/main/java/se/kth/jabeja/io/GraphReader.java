package se.kth.jabeja.io;

import org.apache.log4j.Logger;
import se.kth.jabeja.Node;
import se.kth.jabeja.rand.RandNoGenerator;
import se.kth.jabeja.config.GraphInitColorPolicy;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by salman on 10/24/16.
 */
public class GraphReader {

  final static Logger logger = Logger.getLogger(GraphReader.class);

  public static final String DELIMETER = " ";
  public static final String EMPTY_STRING = "";

  /**
   * read graph form a file
   * The file format is discussed here
   * http://chriswalshaw.co.uk/jostle/jostle-exe.pdf
   *
   * @param graphFilePath
   * @return
   */
  public HashMap<Integer, Node> readGraph(final String graphFilePath, final GraphInitColorPolicy colorPolicy, final int noOfPartitions) {
    final HashMap<Integer, Node> nodes = new HashMap<Integer, Node>();
    try {
      String strLine;
      FileInputStream fis = new FileInputStream(new File(graphFilePath));
      DataInputStream dis = new DataInputStream(fis);
      BufferedReader br = new BufferedReader(new InputStreamReader(dis));

      int numNodes = 0;
      int numEdges = 0;

      // first uncommented line contain information about
      // number of nodes and number of edges
      while ((strLine = br.readLine()) != null) {
        if (strLine.startsWith("%") || strLine.startsWith("#"))
          continue;

        String[] parts = strLine.split(DELIMETER);
        numNodes = Integer.parseInt(parts[0]);
        numEdges = Integer.parseInt(parts[1]);
        break;
      }

      logger.info(graphFilePath + ". Nodes: " + numNodes + ", Edges: " + numEdges);

      int id = 0;
      int partitionSize = numNodes / noOfPartitions;

      while ((strLine = br.readLine()) != null) {

        id++;
        ArrayList<Integer> neighbours = new ArrayList<Integer>();

        if (strLine.startsWith("%") || strLine.startsWith("#")) {
          continue;
        }

        String[] parts = strLine.split(DELIMETER);
        for (int i = 0; i < parts.length; i++) {
          if (parts[i].equals(EMPTY_STRING)) {
            continue;
          }
          neighbours.add(Integer.parseInt(parts[i]));
        }


        int color = getColor(numNodes, noOfPartitions, id, colorPolicy);

        Node node = new Node(id, color);
        node.setNeighbours(neighbours);
        nodes.put(id, node);
      }

      fis.close();
    } catch (IOException e) {
      System.err.println("can not read from file " + graphFilePath);
    }
    printColorDistribution(nodes);
    return nodes;
  }


  /**
   * Generate a color according to the policy.
   * The range of colors are [0, numPartitions)
   *
   * @param numNodes
   * @param numPartitions
   * @param id
   * @param colorPolicy
   * @return color
   */
  private int getColor(int numNodes, int numPartitions, int id, GraphInitColorPolicy colorPolicy) {
    if (colorPolicy == GraphInitColorPolicy.BATCH) {
      double partitionSize = (double) numNodes / (double) numPartitions;
      for (int i = 0; i < numPartitions; i++) {
        double upperLimit = (i + 1) * partitionSize;
        if (id <= upperLimit) {
          return i;
        }
      }
      throw new IllegalStateException(colorPolicy + " Unable to determine color for id: " + id);
    } else if (colorPolicy == GraphInitColorPolicy.RANDOM) {
      return RandNoGenerator.nextInt(numPartitions);

    } else if (colorPolicy == GraphInitColorPolicy.ROUND_ROBIN) {
      return id % numPartitions;
    } else {
      throw new UnsupportedOperationException(colorPolicy + " for color inital color selection is not not implemented");
    }
  }

  /**
   * Prints the distribution of the colors of the graph
   *
   * @param graph input graph
   */
  private void printColorDistribution(HashMap<Integer, Node> graph) {
    Map<Integer, Integer> distribution = new HashMap<Integer, Integer>();
    for (int i : graph.keySet()) {
      int color = graph.get(i).getColor();
      Integer count = distribution.get(color);
      if (count == null) {
        count = new Integer(0);
      }
      distribution.put(color, new Integer(count + 1));
    }

    StringBuffer sb = new StringBuffer("Color Distribution : ");
    for (int i : distribution.keySet()) {
      int count = distribution.get(i);
      sb.append("[ Color: ").append(i).append(",").append(" Count: ").append(count).append(" ] ");
    }

    logger.info(sb);
  }
}
