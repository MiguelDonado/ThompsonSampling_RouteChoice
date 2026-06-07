# This file stores constants, hyperparameters used throughout the project

from dataclasses import dataclass, field
from enum import Enum

import yaml

CONFIG = "/home/miguel/6.Projects/BayesianFinalProject/src/configs/first_koh.yaml"


class Mode(Enum):
    MONTE_CARLO = "montecarlo"
    THOMPSON = "thompson"


@dataclass
class Config:
    network: str
    duration: int
    n_veh: int
    name_network: str
    routes: list[list[str]]
    true_means_tt: list[float]

    ##############
    ### Randomness rng object
    ##############
    seed: int = 42

    ##############
    ### Simulation
    ##############
    mode: Mode = Mode.MONTE_CARLO

    ##############
    ### Agent
    ##############
    departure_time: int = 360

    ##############
    ### MonteCarlo approximation true reward distributions
    ##############
    n_episodes_MC: int = 10

    ##############
    ### Thompson-sampling
    ##############
    n_episodes_TS: int = 50
    true_alpha: float = 1.5  # Parameter gamma distribution
    # Hyperparameters of non-informative prior of beta parameter of Gamma
    prior_a: float = 1
    prior_b: float = 1


# Initialize config
with open(CONFIG, "r") as f:
    data = yaml.safe_load(f)

config = Config(**data)
