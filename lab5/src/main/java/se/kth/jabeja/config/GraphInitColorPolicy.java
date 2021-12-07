package se.kth.jabeja.config;

/**
 * Created by salman on 10/25/16.
 */

/**
 * When the graph is initialized the nodes are assigned some color
 * according to the following config
 */
public enum GraphInitColorPolicy {
    /**
     * Randomly assign a color to the node
     */
    RANDOM("RANDOM"),
    /**
     * Use round robin color assignment
     */
    ROUND_ROBIN("ROUND_ROBIN"),
    /**
     * Assign color in batch. If N nodes and K partitions
     * then first N/K nodes are assigned the same color and
     * then next N/K nodes are assigned the other color, so on
     */
    BATCH("BATCH");

    String name;

    GraphInitColorPolicy(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name;
    }
}
