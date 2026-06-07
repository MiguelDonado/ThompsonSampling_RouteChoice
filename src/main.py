import numpy as np

from config import Mode, config
from montecarlo import approximate_travel_times_distribution
from thompson_sampling import run_thompson_sampling

# Reproducibility
rng = np.random.default_rng(config.seed)
seeds = rng.integers(0, 100000, size=config.n_episodes_MC + config.n_episodes_TS)


def main():
    if config.mode == Mode.MONTE_CARLO:
        # Monte Carlo approximation of travel times distribution of routes
        approximate_travel_times_distribution(seeds)

    elif config.mode == Mode.THOMPSON:
        # Run Thompson Sampling to make right decisions
        run_thompson_sampling(seeds)


if __name__ == "__main__":
    main()
