import os

import mlflow
import numpy as np

from config import Mode, config
from mlflow_utils import log_simulation_mlflow, set_up_mlflow
from montecarlo import approximate_travel_times_distribution
from thompson_sampling import run_thompson_sampling

# Reproducibility
rng = np.random.default_rng(config.seed)
seeds = rng.integers(0, 100000, size=config.n_episodes_MC + config.n_episodes_TS)


def main():

    set_up_mlflow()
    with mlflow.start_run() as run:
        if config.mode == Mode.MONTE_CARLO:
            # Monte Carlo approximation of travel times distribution of routes
            approximate_travel_times_distribution(seeds)

        elif config.mode == Mode.THOMPSON:
            # Run Thompson Sampling to make right decisions
            run_thompson_sampling(seeds)

    # -----------------------------
    # MLflow (Artifact storage)
    # -----------------------------
    log_simulation_mlflow()

    # Play sound to signal end of script
    os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga")


if __name__ == "__main__":
    main()
