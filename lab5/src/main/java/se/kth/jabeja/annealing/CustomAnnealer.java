package se.kth.jabeja.annealing;

import java.util.Random;

import static java.lang.Math.exp;
import static java.lang.Math.log;

public class CustomAnnealer extends NonLinearAnnealer{
    private final Random randomGenerator = new Random();

    CustomAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
    }

    @Override
    protected Double acceptanceProbability(Double oldCost, Double newCost, float temperature){
        return exp(
                (log(newCost) - log(oldCost)) / temperature
        );
    }
}
