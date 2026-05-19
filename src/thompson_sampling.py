import numpy as np
from config import config


class RouteThompsonSampler:
    def __init__(self, alpha, true_mean_tt):

        self.alpha = alpha
        self.true_mean_tt = true_mean_tt

        # PRIOR for beta
        self.prior_a = config.prior_a
        self.prior_b = config.prior_b

        # POSTERIOR parameters
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
        sampled_betas = self.sample_beta_from_posterior(n_samples)
        expected_time_samples = self.alpha / sampled_betas
        self.posterior_mean_meantt = np.mean(expected_time_samples)
        return expected_time_samples
