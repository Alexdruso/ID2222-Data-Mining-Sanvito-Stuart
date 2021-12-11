package se.kth.jabeja.annealing;

import se.kth.jabeja.Node;

import java.util.*;

import static java.lang.Math.pow;

public abstract class Annealer {

    protected float temperature;
    protected float delta;
    protected float alpha;
    protected final Random randomGenerator = new Random();

    Annealer(float temperature, float delta, float alpha){
        this.temperature = temperature;
        this.delta = delta;
        this.alpha = alpha;
    }

    public void setTemperature(float temperature) {
        this.temperature = temperature;
    }

    public void coolDown(){
        if (temperature > 1) temperature -= delta;
        else temperature = 1;
    }

    protected abstract Double acceptanceProbability(Double oldCost, Double newCost, float temperature);

    public Optional<Node> findPartner(
            Node node,
            Node[] candidates,
            HashMap<Integer, Node> entireGraph){
        return Arrays.stream(candidates)
                .filter(
                        candidate -> acceptanceProbability(
                                getCost(node, node.getColor(), candidate, candidate.getColor(), entireGraph),
                                getCost(node, candidate.getColor(), candidate, node.getColor(), entireGraph),
                                temperature
                        ) > randomGenerator.nextDouble()
                )
                .max(
                        Comparator.comparingDouble(
                                candidate -> getCost(
                                        node,
                                        candidate.getColor(),
                                        candidate,
                                        node.getColor(),
                                        entireGraph
                                )
                        )
                );
    }

    protected Double getCost(
            Node nodeP,
            int nodePColor,
            Node nodeQ,
            int nodeQColor,
            HashMap<Integer, Node> entireGraph
    ){
        return pow(getDegree(nodeP, nodePColor, entireGraph), alpha)
                + pow(getDegree(nodeQ, nodeQColor, entireGraph), alpha);
    }

    protected int getDegree(Node node, int colorId, HashMap<Integer, Node> entireGraph){
        return (int) node
                .getNeighbours()
                .stream()
                .map(entireGraph::get)
                .filter(neighbour -> neighbour.getColor() == colorId)
                .count();
    }
}
