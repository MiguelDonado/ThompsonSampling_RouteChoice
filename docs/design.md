- The background traffic should be different for each episode, otherwise travel times would be deterministic, and we do not want that. We want travel times to be realizations of a hidden distribution. We need uncertainty to learn

- Free flow travel times: Would be used to compare routes fairly. We can see that a route has lower free flow than others, but it has higher mean tt, meaning that with the empty network we would prefer A, but with the network congested, B is better.

- Important details for Thompson Sampling to be relevant
  1. Means relatively close
  2. Distributions overlap
  3. Uncertainty matters
   

For Thompson Sampling, Im interested in Posterior distribution of expected travel time because the action-selection rule is based on samples from this posterior, not in the posterior distribution of travel times.

https://github.com/lilianweng/multi-armed-bandit
https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/

Put bibliography in the latex document