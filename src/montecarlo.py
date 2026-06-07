import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import skew

from config import config
from environment import Environment
from paths import REWARD_DISTRIBUTIONS_DIR, TRAVEL_TIMES_MONTECARLO
from scenario import Scenario


def approximate_travel_times_distribution(seeds):
    """
    All logic to perform Monte Carlo approximation of
    the travel times distributions of the different routes
    """

    print("\nMonte Carlo Approximation of travel time distributions\n")

    # For each route
    for idx_route, _ in enumerate(config.routes):
        print(f"####### Route {idx_route} #######\n")
        # 1. Generate samples from travel time distribution
        travel_times = generate_montecarlo_simulations(idx_route, seeds)

        # 2. Generate plot (histogram + KDE)
        path_hist = (
            REWARD_DISTRIBUTIONS_DIR / config.name_network / f"route_{idx_route}.png"
        )
        plot_histogram_and_kde_tt(travel_times, path=path_hist, idx_route=idx_route)


def generate_montecarlo_simulations(idx_route, seeds):
    """
    This function produces a parquet file containing the montecarlo simulations of the
    distribution of travel times for the different routes
    """
    travel_times = []

    for episode in range(1, config.n_episodes_MC + 1):
        print(f"--- Episode {episode} ---")
        scen = Scenario(config.network, seed=seeds[episode - 1], episode=episode)
        env = Environment(scen)
        env.agent_select_action(config.routes, selected_route=idx_route)
        env.run_episode()
        agent_tt = env.get_reward()
        print(f"Travel time: {agent_tt}\n")
        travel_times.append(agent_tt)

    # Save parquet file with travel times samples
    df = pd.DataFrame(
        zip(range(1, config.n_episodes_MC + 1), travel_times),
        columns=["episode", "travel_time"],
    )
    path_df = (
        TRAVEL_TIMES_MONTECARLO
        / config.name_network
        / f"tt_MonteCarlo_route{idx_route}.parquet"
    )
    df.to_parquet(path_df)
    return travel_times


def plot_histogram_and_kde_tt(tt, path, idx_route):
    # 1. Compute sample mean and sample sd
    mean = np.mean(tt)
    std = np.std(tt)

    # 2. Compute sample skewness
    skewness = skew(tt)

    # 3. Compute sample quantiles
    q50 = np.percentile(tt, 50)
    q90 = np.percentile(tt, 90)
    q95 = np.percentile(tt, 95)

    # 4. Plot histogram + KDE
    sns.histplot(tt, bins="fd", stat="density", kde=True)

    # 5. Add annotations to the plot
    plt.plot([], [], " ", label=f"Mean = {mean:.2f}")
    plt.plot([], [], " ", label=f"Std = {std:.2f}")
    plt.plot([], [], " ", label=f"Skew = {skewness:.2f}")

    plt.plot([], [], " ", label=f"Q50 = {q50:.2f}")
    plt.plot([], [], " ", label=f"Q90 = {q90:.2f}")
    plt.plot([], [], " ", label=f"Q95 = {q95:.2f}")

    # 6. Configure labels plot
    plt.xlabel("Travel time")
    plt.ylabel("Density")

    # 7. Configure title
    plt.title(
        f"Route {idx_route} travel time distribution\n"
        f"(Monte Carlo approximation using {config.n_episodes_MC} simulations"
    )

    # 8. Remove legend
    plt.legend()

    # 9. Save plot
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
