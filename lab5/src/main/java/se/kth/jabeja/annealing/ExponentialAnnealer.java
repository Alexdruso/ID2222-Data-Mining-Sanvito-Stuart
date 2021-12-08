package se.kth.jabeja.annealing;

import se.kth.jabeja.Node;

import java.util.HashMap;
import java.util.Optional;

public class ExponentialAnnealer extends Annealer {
    ExponentialAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
    }

    @Override
    public Optional<Node> findPartner(Node node, Node[] candidates, HashMap<Integer, Node> entireGraph) {
        return Optional.empty();
    }
}
