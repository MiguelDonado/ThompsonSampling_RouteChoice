import numpy as np


class RouteThompsonSampler:
    def __init__(self, alpha):

        self.alpha = alpha

        # PRIOR for beta
        self.prior_a = 1
        self.prior_b = 1

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
        return expected_time_samples
