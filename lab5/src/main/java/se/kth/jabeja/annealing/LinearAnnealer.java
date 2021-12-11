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
    protected Double acceptanceProbability(Double oldCost, Double newCost, float temperature) {
        return temperature*(newCost) > oldCost? 1.0 : 0.0;
    }
}
