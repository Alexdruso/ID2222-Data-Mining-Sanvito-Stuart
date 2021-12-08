package se.kth.jabeja.annealing;

import se.kth.jabeja.Node;

import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Optional;

public class LinearAnnealer extends Annealer {
    LinearAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
    }

    @Override
    public Optional<Node> findPartner(Node node, Node[] candidates, HashMap<Integer, Node> entireGraph) {
        return Arrays.stream(candidates)
                .filter(
                        candidate -> temperature * getCost(
                                node,
                                candidate.getColor(),
                                candidate,
                                node.getColor(),
                                entireGraph
                        ) > getCost(
                                node,
                                node.getColor(),
                                candidate,
                                candidate.getColor(),
                                entireGraph
                        )
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
}
