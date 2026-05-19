from config import config
from scenario import Scenario
from environment import Environment
from data_science import plot_histogram_tt
from paths import REWARD_DISTRIBUTIONS_DIR


def approximate_reward_distributions(seeds):
    print("Monte Carlo Approximation of reward distributions\n")
    for idx_route, _ in enumerate(config.routes):
        path = REWARD_DISTRIBUTIONS_DIR / f"route_{idx_route}.png"
        travel_times = []

        for episode in range(1, config.n_episodes + 1):
            print(f"--- Episode {episode} ---")
            scen = Scenario(config.network, seed=seeds[episode - 1], episode=episode)
            env = Environment(scen)
            env.agent_select_action(config.routes, selected_route=idx_route)
            env.run_episode()
            agent_tt = env.get_reward()
            print(agent_tt)
            travel_times.append(agent_tt)

        # Plot histogram
        plot_histogram_tt(travel_times, path=path)


def perform_simulation(seeds, episode, selected_route):
    scen = Scenario(config.network, seed=seeds[episode - 1], episode=episode)
    env = Environment(scen)
    env.agent_select_action(config.routes, selected_route=selected_route)
    env.run_episode()
    agent_tt = env.get_reward()
    return agent_tt
