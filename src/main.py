from scenario import Scenario
from environment import Environment
from config import config
from data_science import plot_histogram_tt
import numpy as np
from utils import approximate_reward_distributions, perform_simulation
from thompson_sampling import RouteThompsonSampler

# Reproducibility
rng = np.random.default_rng(config.seed)
seeds = rng.integers(
    0, 100000, size=config.n_episodes + config.n_episodes_thompson_sampling
)


def main():
    # Monte Carlo approximation travel times distribution of routes
    approximate_reward_distributions(seeds)

    # Initialize Route Thompson Sampler
    routes = [RouteThompsonSampler(alpha=config.true_alpha) for route in config.routes]

    for episode in range(1, config.n_episodes_thompson_sampling + 1):
        print(f"--- Episode {episode} ---")
        # sample expected travel time from each posterior
        sampled_times = [r.sample_expected_travel_time() for r in routes]

        # choose route with MINIMUM sampled avg travel time
        chosen_idx = np.argmin(sampled_times)

        # observe actual travel time
        agent_tt = perform_simulation(seeds, episode, selected_route=chosen_idx)

        # update posterior
        routes[chosen_idx].update_posterior(agent_tt)


if __name__ == "__main__":
    main()
