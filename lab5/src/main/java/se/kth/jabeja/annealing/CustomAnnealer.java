package se.kth.jabeja.annealing;

import se.kth.jabeja.Node;

import java.util.HashMap;
import java.util.Optional;

public class CustomAnnealer extends Annealer{
    CustomAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
    }

    @Override
    public Optional<Node> findPartner(Node node, Node[] candidates, HashMap<Integer, Node> entireGraph) {
        return Optional.empty();
    }
}
