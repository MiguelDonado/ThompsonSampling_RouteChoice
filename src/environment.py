"""
Class responsible for running the simulation
"""

from config import config
from paths import ROUTES, TRIPS_INFO

import subprocess
from lxml import etree


class Environment:
    def __init__(self, scenario):
        self.scenario = scenario

    def agent_select_action(self, routes, selected_route):
        action = routes[selected_route]
        # Update route file with the selected route
        self._update_routes(action)

    def run_episode(self):
        cmd = ["sumo", self.scenario.conf]
        subprocess.run(cmd)

    def get_reward(self):
        tree = etree.parse(TRIPS_INFO)
        root = tree.getroot()
        agent_tt = float(root.xpath("//tripinfo[@id='agent']/@duration")[0])
        return agent_tt

    ###################
    # Helper functionsROUTES
    ###################
    def _select_action_using_strategy(self, routes):
        action = routes[0]
        return action

    def _update_routes(self, action):
        tree = etree.parse(ROUTES)
        root = tree.getroot()

        # Convert route list into SUMO edge string
        action = " ".join(action)

        # Get agent vehicle
        agent = root.xpath("//vehicle[@id='agent']")[0]

        # Remove old route if it exists
        old_route = agent.find("route")

        if old_route is not None:
            agent.remove(old_route)

        # Create new route
        route = etree.SubElement(agent, "route")
        route.set("edges", action)

        # Pretty formatting
        etree.indent(tree, space="    ")

        # Save
        tree.write(
            ROUTES,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8",
        )
