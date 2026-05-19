# This file stores constants, hyperparameters used throughout the project

from dataclasses import dataclass, field
from enum import Enum

"""
Routes:
1st network:
["E1_2_EB","E2_3_EB","E3_6_NWB","E6_7_EB"]
["E1_2_EB","E2_5_NB","E5_6_NEB","E6_7_EB"]
["E1_2_EB","E2_3_EB","E3_5_NWB","E5_6_NEB","E6_7_EB"]
"""


@dataclass
class Config:
    network: str = (
        "/home/miguel/6.Projects/BayesianFinalProject/sumo/networks/1st.net.xml"
    )
    duration: int = 1200
    n_veh: int = 1
    routes: list[list[str]] = field(default_factory=list)
    n_episodes: int = 100
    seed: int = 42

    # Agent
    departure_time: int = 600


config = Config(
    routes=[
        ["E1_2_EB", "E2_3_EB", "E3_6_NWB", "E6_7_EB"],
        ["E1_2_EB", "E2_5_NB", "E5_6_NEB", "E6_7_EB"],
        ["E1_2_EB", "E2_3_EB", "E3_5_NWB", "E5_6_NEB", "E6_7_EB"],
    ]
)
