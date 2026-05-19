"""
Class that creates the routes, config file
"""

from paths import SUMO_CONF, TRIPS_INFO, ROUTES, UNDESIRED_FILE
import subprocess
from config import config
from lxml import etree


class Scenario:
    def __init__(self, network, seed):
        self.network = network
        self.seed = seed

        self.generate_bg_traffic(config.duration, config.n_veh, self.seed)
        self.insert_agent(config.departure_time)
        self.conf = self.generate_conf(self.network, ROUTES)

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
