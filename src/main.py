from scenario import Scenario
from environment import Environment
from config import config
import numpy as np

# Reproducibility
rng = np.random.default_rng(config.seed)
seeds = rng.integers(0, 100000, size=config.n_episodes)


def main():
    for episode in range(1, config.n_episodes + 1):
        scen = Scenario(config.network, seed=seeds[episode - 1])
        env = Environment(scen)
        env.agent_select_action(config.routes)
        env.run_episode()
        agent_tt = env.get_reward()
        print(agent_tt)


if __name__ == "__main__":
    main()
