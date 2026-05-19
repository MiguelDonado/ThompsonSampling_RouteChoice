from config import config
from scenario import Scenario
from environment import Environment
from data_science import plot_histogram_and_kde_tt
from paths import REWARD_DISTRIBUTIONS_DIR, TRAVEL_TIMES_MONTECARLO
import pandas as pd


def approximate_reward_distributions(seeds):
    print("\nMonte Carlo Approximation of reward distributions\n")
    for idx_route, _ in enumerate(config.routes):
        print(f"####### Route {idx_route} #######\n")
        path = REWARD_DISTRIBUTIONS_DIR / config.name_network / f"route_{idx_route}.png"
        travel_times = []

        for episode in range(1, config.n_episodes + 1):
            print(f"--- Episode {episode} ---")
            scen = Scenario(config.network, seed=seeds[episode - 1], episode=episode)
            env = Environment(scen)
            env.agent_select_action(config.routes, selected_route=idx_route)
            env.run_episode()
            agent_tt = env.get_reward()
            print(f"Travel time: {agent_tt}\n")
            travel_times.append(agent_tt)

        # Save parquet file with samples travel times
        df = pd.DataFrame(
            zip(range(1, config.n_episodes + 1), travel_times),
            columns=["episode", "travel_time"],
        )
        path_df = (
            TRAVEL_TIMES_MONTECARLO
            / config.name_network
            / f"tt_MonteCarlo_route{idx_route}.parquet"
        )
        df.to_parquet(path_df)
        print(f"Monte Carlo travel times saved in {path_df}")
        # Plot histogram
        plot_histogram_and_kde_tt(travel_times, path=path, idx_route=idx_route)


def perform_simulation(seeds, episode, selected_route):
    scen = Scenario(config.network, seed=seeds[episode - 1], episode=episode)
    env = Environment(scen)
    env.agent_select_action(config.routes, selected_route=selected_route)
    env.run_episode()
    agent_tt = env.get_reward()
    return agent_tt
