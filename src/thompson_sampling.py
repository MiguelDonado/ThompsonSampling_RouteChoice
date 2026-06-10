import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from config import config
from environment import Environment
from paths import CONVERGENCE_POST_MEANS, POST_AVG_TT_DIR
from scenario import Scenario


class RouteThompsonSampler:
    def __init__(self, alpha, true_mean_tt):
        """
        This class implements the logic of a Thompson Sampler

        0. Model travel times using a gamma(alpha, beta)
           with alpha known and beta unknown

        1. Define prior and posterior distributions over beta parameter

        2. Sample beta from posteriors

        3. Get sample expected travel time

        4. Update posteriors with observed travel time

        5. Get samples posterior expected travel time

        6. Compute posterior mean expected travel time

        Mathematical mode: shape-rate Gamma
        NumPy implementation: shape-scale Gamma

        Thats why I then transformed scale = 1 / beta
        """

        self.alpha = alpha
        self.true_mean_tt = true_mean_tt

        # Hyperprior parameters for beta
        self.prior_a = config.prior_a
        self.prior_b = config.prior_b

        # Hyperposterior parameters
        self.post_a = self.prior_a
        self.post_b = self.prior_b

    def sample_beta_from_posterior(self, n_samples):
        sampled_beta = np.random.gamma(
            shape=self.post_a, scale=1 / self.post_b, size=n_samples
        )
        return sampled_beta

    def sample_expected_travel_time(self, n_samples):
        sampled_beta = self.sample_beta_from_posterior(n_samples)

        sampled_mean = self.alpha / sampled_beta

        return sampled_mean

    def update_posterior(self, tt):
        self.post_a = self.post_a + self.alpha
        self.post_b = self.post_b + tt

    def get_samples_post_avg_tt(self, n_samples):
        """
        Generate samples from posterior distribution of expected travel time
        It also computes posterior mean
        """
        sampled_betas = self.sample_beta_from_posterior(n_samples)
        expected_time_samples = self.alpha / sampled_betas

        # Compute posterior mean
        self.compute_posterior_mean_meantt(expected_time_samples)
        return expected_time_samples

    def compute_posterior_mean_meantt(self, expected_time_samples):
        """
        Compute the posterior mean of expected travel time
        """
        self.posterior_mean_meantt = np.mean(expected_time_samples)


def run_thompson_sampling(seeds):
    n_samples_posterior = 1000

    # 0. Initialize for each route a Thompson Sampler
    routes = [
        RouteThompsonSampler(
            alpha=config.MoM_alpha[idx], true_mean_tt=config.true_means_tt[idx]
        )
        for idx, _ in enumerate(config.routes)
    ]

    for episode in range(1, config.n_episodes_TS + 1):
        print(f"\n--- Episode {episode} ---")

        # 1. Generate plot with all posterior distributions
        plot_posterior_distributions_avg_tt(
            i=episode, routes=routes, n_samples=n_samples_posterior
        )

        # 2. Sample from each posterior
        sampled_times = [r.sample_expected_travel_time(n_samples=1) for r in routes]
        print(f"\t- Sampled mean travel times of routes: {sampled_times}")

        # 3. Choose route that maximizes reward
        # Reward = -Travel time
        sampled_rewards = [-sample_time for sample_time in sampled_times]
        chosen_idx = np.argmax(sampled_rewards)
        print(f"\t- Chosen route: {chosen_idx}")

        # 4. Observe actual travel time
        agent_tt = simulate_episode(seeds, episode, selected_route=chosen_idx)
        print(f"\t- Observed travel time: {agent_tt}")

        # 5. Update posterior (only of chosen route)
        routes[chosen_idx].update_posterior(agent_tt)

    # 6. Generate plot comparing post mean obtained after convergence with the true means
    plot_convergence_post_mean_meantt(R=routes)


def plot_posterior_distributions_avg_tt(i, routes, n_samples):
    """
    Generates a plot that contains all the posterior distributions
    """
    # 1. Condition to plot the post dist
    #   Episode must meet some of the next criteria
    #   a) < 10
    #   b) If < 100 then (i + 1) % 10 == 0
    #   c) (i + 1) % 100 == 0
    if i < 10 or (i < 100 and (i + 1) % 10 == 0) or ((i + 1) % 100 == 0):

        # 2. Path of the plot
        path = POST_AVG_TT_DIR / config.name_network / f"post_avg_tt_{i}.png"

        # 3. Plot posterior distribution for each route
        for route in routes:
            samples = route.get_samples_post_avg_tt(n_samples)
            sns.kdeplot(samples, fill=True)

        # 4. Annotations
        plt.legend([f"true_mean_tt={r.true_mean_tt}" for r in routes], fontsize=16)

        # 5. Title
        plt.title(
            f"Iterarion {i}\n" "Posterior distributions of mean travel time",
            fontsize=20,
        )

        # 6. Axis
        plt.xlim(50, 200)
        plt.xlabel("Mean Travel Time", fontsize=20)
        plt.ylabel("Density", fontsize=20)

        # 7. Save
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()


def simulate_episode(seeds, episode, selected_route):
    scen = Scenario(config.network, seed=seeds[episode - 1], episode=episode)
    env = Environment(scen)
    env.agent_select_action(config.routes, selected_route=selected_route)
    env.run_episode()
    agent_tt = env.get_reward()
    return agent_tt


def plot_convergence_post_mean_meantt(R):
    """
    Generates a plot that compares the true hidden avg rewards
    with the posterior means after convergence
    """
    path = CONVERGENCE_POST_MEANS

    plt.figure(figsize=(5, 5))
    true_means = [r.true_mean_tt for r in R]
    posterior_means = [r.posterior_mean_meantt for r in R]

    plt.scatter(true_means, posterior_means)
    # Diagonal line
    plt.plot(true_means, true_means, color="k", alpha=0.5, linestyle="--")

    plt.xlabel("True Mean", fontsize=20)
    plt.ylabel("Posterior Mean", fontsize=20)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
