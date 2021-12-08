package se.kth.jabeja.annealing;

import se.kth.jabeja.Node;

import java.util.HashMap;
import java.util.Optional;

import static java.lang.Math.pow;

public abstract class Annealer {
    protected float temperature;
    protected float delta;
    protected float alpha;

    Annealer(float temperature, float delta, float alpha){
        this.temperature = temperature;
        this.delta = delta;
        this.alpha = alpha;
    }

    public void coolDown(){
        if (temperature > 1) temperature -= delta;
        else temperature = 1;
    }

    public abstract Optional<Node> findPartner(Node node, Node[] candidates, HashMap<Integer, Node> entireGraph);

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
