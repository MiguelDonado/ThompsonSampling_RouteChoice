# This file stores constants, hyperparameters used throughout the project

from dataclasses import dataclass, field
from enum import Enum

import numpy as np
import yaml
from lxml import etree

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
    true_std_tt: list[float]
    MoM_alpha: list[float]
    departure_time: int

    ##############
    ### Randomness rng object
    ##############
    seed: int = 42

    ##############
    ### Simulation
    ##############
    mode: Mode = Mode.THOMPSON

    ##############
    ### MonteCarlo approximation true reward distributions
    ##############
    n_episodes_MC: int = 50

    ##############
    ### Thompson-sampling
    ##############
    n_episodes_TS: int = 50
    # Hyperparameters of non-informative prior of beta parameter of Gamma
    prior_a: float = 1
    prior_b: float = 1


# Initialize config
with open(CONFIG, "r") as f:
    data = yaml.safe_load(f)

config = Config(**data)
