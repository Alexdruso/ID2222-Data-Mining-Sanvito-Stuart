package se.kth.jabeja.annealing;

import static java.lang.Math.exp;

public class ExponentialAnnealer extends NonLinearAnnealer {

    ExponentialAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
    }

    @Override
    protected Double acceptanceProbability(Double oldCost, Double newCost, float temperature){
        return exp(
                (newCost - oldCost) / temperature
        );
    }
}
