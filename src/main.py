from scenario import Scenario
from environment import Environment
from config import config
from data_science import plot_histogram_tt
import numpy as np
from utils import approximate_reward_distributions

# Reproducibility
rng = np.random.default_rng(config.seed)
seeds = rng.integers(0, 100000, size=config.n_episodes)


def main():
    approximate_reward_distributions(seeds)


if __name__ == "__main__":
    main()
