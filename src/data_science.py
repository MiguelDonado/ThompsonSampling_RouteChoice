import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew


def plot_histogram_tt(tt, path):
    mean = np.mean(tt)
    std = np.std(tt)

    # Skewness
    skewness = skew(tt)

    # Quantiles
    q50 = np.percentile(tt, 50)
    q90 = np.percentile(tt, 90)
    q95 = np.percentile(tt, 95)

    plt.hist(tt, bins="fd")

    # Legend entries only
    plt.plot([], [], " ", label=f"Mean = {mean:.2f}")
    plt.plot([], [], " ", label=f"Std = {std:.2f}")
    plt.plot([], [], " ", label=f"Skew = {skewness:.2f}")

    plt.plot([], [], " ", label=f"Q50 = {q50:.2f}")
    plt.plot([], [], " ", label=f"Q90 = {q90:.2f}")
    plt.plot([], [], " ", label=f"Q95 = {q95:.2f}")

    plt.xlabel("Agent travel time")
    plt.ylabel("Frequency")
    plt.title("Route travel time distribution")

    plt.legend()

    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
