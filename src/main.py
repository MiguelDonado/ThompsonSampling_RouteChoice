from scenario import Scenario
from environment import Environment
from config import config
from data_science import plot_histogram_tt
import numpy as np

# Reproducibility
rng = np.random.default_rng(config.seed)
seeds = rng.integers(0, 100000, size=config.n_episodes)


def main():
    travel_times = []
    for episode in range(1, config.n_episodes + 1):
        print(f"--- Episode {episode} ---")
        scen = Scenario(config.network, seed=seeds[episode - 1], episode=episode)
        env = Environment(scen)
        env.agent_select_action(config.routes)
        env.run_episode()
        agent_tt = env.get_reward()
        print(agent_tt)
        travel_times.append(agent_tt)

    # Plot histogram
    plot_histogram_tt(travel_times, 5)


if __name__ == "__main__":
    main()
