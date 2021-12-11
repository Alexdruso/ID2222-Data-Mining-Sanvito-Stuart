package se.kth.jabeja.annealing;

public abstract class NonLinearAnnealer extends Annealer{

    NonLinearAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
        this.temperature = temperature > 1? 1 : temperature;
    }

    @Override
    public void coolDown() {
        temperature *= delta;
    }
}
