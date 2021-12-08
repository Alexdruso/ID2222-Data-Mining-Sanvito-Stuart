package se.kth.jabeja.annealing;

public enum AnnealingType {
    LINEAR {
        @Override
        public Annealer getAnnealer(float temperature, float delta, float alpha) {
            return new LinearAnnealer(temperature, delta, alpha);
        }
    },
    EXPONENTIAL {
        @Override
        public Annealer getAnnealer(float temperature, float delta, float alpha) {
            return new ExponentialAnnealer(temperature, delta, alpha);
        }
    };

    public abstract Annealer getAnnealer(float temperature, float delta, float alpha);
}
