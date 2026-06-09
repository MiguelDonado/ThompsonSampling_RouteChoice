import numpy as np
import pandas as pd
import yaml
from lxml import etree

# Set config file
CONFIG = "/home/miguel/6.Projects/BayesianFinalProject/src/configs/first_koh.yaml"

# Load data config
with open(CONFIG, "r") as f:
    data = yaml.safe_load(f)


# CONSTANTS
NETWORK_PATH = data["network"]
ROUTES = data["routes"]

MEAN_TT = data["true_means_tt"]
STD_TT = data["true_std_tt"]


def get_edges_lengths_script():
    ###########
    # SCRIPT
    ###########

    document = NETWORK_PATH
    tree = etree.parse(document)

    # Edge ids
    edge_ids = tree.xpath("//edge[not(@function='internal')]/@id")

    # Length edges
    edges_length = tree.xpath("//edge[not(@function='internal')]/lane/@length")
    edges_length = [float(edge_length) for edge_length in edges_length]

    # Speed edges
    edges_speed = tree.xpath("//edge[not(@function='internal')]/lane/@speed")
    edges_speed = [float(edge_speed) for edge_speed in edges_speed]

    # Free-flow travel time edges
    edges_fftt = [
        float(length / speed) for length, speed in zip(edges_length, edges_speed)
    ]

    # Dictionaries
    length_dict = dict(zip(edge_ids, edges_length))
    fftt_dict = dict(zip(edge_ids, edges_fftt))

    # Compute route lengths
    route_lengths = [sum(length_dict[edge] for edge in route) for route in ROUTES]

    # Compute free-flow travel times
    route_fftt = [sum(fftt_dict[edge] for edge in route) for route in ROUTES]

    # Gap (difference between the mean travel time of the optimal route and the mean tt of the current route)
    route_gaps = [mean_route - min(MEAN_TT) for mean_route in MEAN_TT]

    df_routes = pd.DataFrame(
        {
            "Route": [f"Route {i}" for i in range(1, len(route_lengths) + 1)],
            "Length (m)": route_lengths,
            "Free-flow TT (s)": route_fftt,
            "Mean TT (s)": MEAN_TT,
            "Std TT (s)": STD_TT,
            "Gap (s)": route_gaps,
        }
    )

    print(df_routes)


get_edges_lengths_script()
