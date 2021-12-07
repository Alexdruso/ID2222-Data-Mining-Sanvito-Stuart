package se.kth.jabeja.config;

/**
 * Created by salman on 10/25/16.
 */
public enum NodeSelectionPolicy {
    RANDOM("RANDOM"),
    HYBRID("HYBRID"),
    LOCAL("LOCAL");
    String name;
    NodeSelectionPolicy(String name) {
        this.name = name;
    }
    @Override
    public String toString() {
        return name;
    }
}
