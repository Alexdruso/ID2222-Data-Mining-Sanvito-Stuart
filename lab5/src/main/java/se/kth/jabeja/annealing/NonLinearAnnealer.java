package se.kth.jabeja.annealing;

import se.kth.jabeja.Node;

import java.util.*;

public abstract class NonLinearAnnealer extends Annealer{
    protected final Random randomGenerator = new Random();

    NonLinearAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
    }

    @Override
    public void coolDown() {
        if (temperature > 0.00001) temperature *= delta;
        else temperature = (float) 0.00001;
    }

    protected abstract Double acceptanceProbability(Double oldCost, Double newCost, float temperature);

    @Override
    public Optional<Node> findPartner(Node node, Node[] candidates, HashMap<Integer, Node> entireGraph) {
        Optional<Node> result = Arrays.stream(candidates)
                .filter(
                        candidate -> getCost(
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

        if(!result.isPresent())
            result = Arrays.stream(candidates)
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

        return result;
    }
}
