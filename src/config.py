# This file stores constants, hyperparameters used throughout the project

from dataclasses import dataclass, field
from enum import Enum

"""
1st network:
    OD: 
        1-7
    Routes:
        ["E1_2_EB","E2_6_NB","E6_7_NEB","E7_8_NEB"],
        ["E1_2_EB","E2_3_EB","E3_4_EB","E4_7_NWB","E7_8_NEB"],
        ["E1_2_EB","E2_3_EB","E3_6_NWB","E6_7_NEB","E7_8_NEB"]
    Duration: 
        520
    N_veh: 
        150
    Departure_time:
        360

Sioux Falls:
    OD:
        1-20
    Routes:
        ["E1_3_SB","E3_12_SB","E12_13_SB","E13_24_EB","E21_24_EB","E20_21_EB"],
        ["E1_2_EB","E2_6_SB","E6_8_SB","E8_16_SB","E16_17_SB","E17_19_SB","E19_20_SB"],
    Duration: 
        520
    N_veh:
        450
    Departure_time_
        360

"""


@dataclass
class Config:
    ##############
    ### Randomness rng object
    ##############
    seed: int = 42

    ##############
    ### Simulation
    ##############
    network: str = (
        "/home/miguel/6.Projects/BayesianFinalProject/sumo/networks/1st_koh.net.xml"
    )
    duration: int = 520
    n_veh: int = 150

    ##############
    ### Agent
    ##############
    departure_time: int = 360
    routes: list[list[str]] = field(default_factory=list)

    ##############
    ### MonteCarlo approximation true reward distributions
    ##############
    n_episodes: int = 10
    true_means_tt: list[list[float]] = field(default_factory=list)

    ##############
    ### Thompson-sampling
    ##############
    n_episodes_thompson_sampling: int = 2000
    true_alpha: float = 1.5  # Parameter gamma distribution
    # Non-informative prior over beta parameter of Gamma
    prior_a: float = 0.001
    prior_b: float = 0.001


config = Config(
    routes=[
        ["E1_2_EB", "E2_6_NB", "E6_7_NEB", "E7_8_NEB"],
        ["E1_2_EB", "E2_3_EB", "E3_4_EB", "E4_7_NWB", "E7_8_NEB"],
        ["E1_2_EB", "E2_3_EB", "E3_6_NWB", "E6_7_NEB", "E7_8_NEB"],
    ],
    true_means_tt=[64.5, 72.5, 85],
)
