from scenario import Scenario
from environment import Environment
from config import config
from data_science import draw_distributions
import numpy as np
from utils import approximate_reward_distributions, perform_simulation
from thompson_sampling import RouteThompsonSampler
from pathlib import Path

# Reproducibility
rng = np.random.default_rng(config.seed)
seeds = rng.integers(
    0, 100000, size=config.n_episodes + config.n_episodes_thompson_sampling
)


def main():
    config.name_network = Path(config.network).name.replace(".net.xml", "")

    # Monte Carlo approximation travel times distribution of routes
    approximate_reward_distributions(seeds)

    # Initialize Route Thompson Sampler
    routes = [
        RouteThompsonSampler(
            alpha=config.true_alpha, true_mean_tt=config.true_means_tt[idx]
        )
        for idx, _ in enumerate(config.routes)
    ]

    for episode in range(1, config.n_episodes_thompson_sampling + 1):
        print(f"\n--- Episode {episode} ---")

        draw_distributions(i=episode, R=routes, n_samples=1000)

        # sample expected travel time from each posterior
        sampled_times = [r.sample_expected_travel_time(n_samples=1) for r in routes]
        print(f"\t- Sampled mean travel times of routes: {sampled_times}")

        # choose route with MINIMUM sampled avg travel time (max reward)
        sampled_rewards = [-sample_time for sample_time in sampled_times]
        chosen_idx = np.argmax(sampled_rewards)
        print(f"\t- Chosen route: {chosen_idx}")

        # observe actual travel time
        agent_tt = perform_simulation(seeds, episode, selected_route=chosen_idx)
        print(f"\t- Observed travel time: {agent_tt}")

        # update posterior
        routes[chosen_idx].update_posterior(agent_tt)


if __name__ == "__main__":
    main()
