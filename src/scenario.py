"""
Class that performs the next steps:
    1. Creates the bg traffic, inserts the agent (ROUTES FILE)
    2. Creates the config file
    3. Computes the free flow travel time of routes
"""

import subprocess

import pandas as pd
from lxml import etree

from config import config
from paths import (
    FREE_FLOW_TRAVEL_TIMES_LINKS,
    FREE_FLOW_TRAVEL_TIMES_ROUTES,
    ROUTES,
    SUMO_CONF,
    TRIPS_INFO,
    UNDESIRED_FILE,
)


class Scenario:
    def __init__(self, network, seed, episode):
        self.network = network
        self.seed = seed
        self.ff_tt_routes = []

        self.generate_bg_traffic(config.duration, config.n_veh, self.seed)
        self.insert_agent(config.departure_time)
        self.conf = self.generate_conf(self.network, ROUTES)

        # Only for the first episode
        if episode == 1:
            self.generate_free_flow_tt_routes(config.routes)

    def generate_bg_traffic(self, duration, n_veh, seed):
        """
        Departure interval calculation:
        Example:
        duration = 1000 seconds
        n_veh = 100
        one vehicle every 10 seconds

        -b: Begin time
        -e: End time
        -p: Generate 1 trip every n seconds
        """
        n = duration / n_veh

        cmd = [
            "randomTrips.py",
            "-n",
            self.network,
            "-b",
            "0",
            "-e",
            str(duration),
            "-p",
            str(n),
            "--seed",
            str(seed),
            "-o",
            ROUTES,
        ]
        subprocess.run(cmd, check=True)
        UNDESIRED_FILE.unlink()

    def insert_agent(self, agent_departure_time):
        """
        Insert agent element in routes XML file
        """
        tree = etree.parse(ROUTES)
        root = tree.getroot()

        # Create agent vehicle
        agent = etree.Element("vehicle")
        agent.set("id", "agent")
        agent.set("depart", str(agent_departure_time))

        # Find insertion index
        insert_idx = len(root)
        for i, elem in enumerate(root):
            if elem.tag in ("trip", "vehicle"):
                depart = float(elem.get("depart"))

                if depart > agent_departure_time:
                    insert_idx = i
                    break

        # Insert vehicle
        root.insert(insert_idx, agent)

        etree.indent(tree, space="    ")

        # Save nicely formatted
        tree.write(
            ROUTES,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8",
        )

    def generate_conf(self, network, routes):
        with open(SUMO_CONF, "w+") as conf:
            conf.write('<?xml version="1.0"?>\n')
            conf.write("<configuration>\n")
            conf.write("\t<input>\n")
            conf.write(f'\t\t<net-file value="{network}"/>\n')
            conf.write(f'\t\t<route-files value="{routes}"/>\n')
            conf.write("\t</input>\n")
            conf.write(f"\t<report>\n")
            conf.write(f'\t\t<tripinfo-output value="{TRIPS_INFO}"/>\n')
            conf.write(f"\t</report>\n")
            conf.write("</configuration>\n")
        return SUMO_CONF

    def generate_free_flow_tt_routes(self, routes):
        """
        Creates a parquet file with columns:
        route_id | free_flow_tt
        """
        self._generate_free_flow_tt_links()
        ff_tt_links = pd.read_parquet(FREE_FLOW_TRAVEL_TIMES_LINKS)
        ff_tt_routes = []
        for i, route in enumerate(routes):
            route_tt = 0
            for edge in route:
                ff_tt_edge_row = ff_tt_links[ff_tt_links["edge"] == edge]
                ff_tt_edge = ff_tt_edge_row.iloc[0]["free_flow_travel_time"]
                route_tt += ff_tt_edge
            ff_tt_routes.append({"route_id": i, "free_flow_tt": route_tt})
        df = pd.DataFrame(ff_tt_routes)
        df.to_parquet(FREE_FLOW_TRAVEL_TIMES_ROUTES, engine="pyarrow", index=False)

    def _generate_free_flow_tt_links(self):
        """
        Called once per program execution
        Creates a parquet file with columns:

        edge | free_flow_travel_time
        """
        data = []

        tree = etree.parse(config.network)
        edges = tree.xpath("//edge[not(@function='internal')]")
        for edge in edges:
            edge_id = edge.get("id")

            lane = edge.find("lane")

            free_flow_speed = float(lane.get("speed"))
            length = float(lane.get("length"))

            free_flow_travel_time = length / free_flow_speed
            data.append(
                {"edge": edge_id, "free_flow_travel_time": free_flow_travel_time}
            )

        df = pd.DataFrame(data)
        df.to_parquet(FREE_FLOW_TRAVEL_TIMES_LINKS, engine="pyarrow", index=False)
