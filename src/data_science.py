import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew
import seaborn as sns
import matplotlib.pyplot as plt


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


def draw_distributions(R, i, n_samples):
    if i < 10 or (i < 100 and (i + 1) % 10 == 0) or ((i + 1) % 100 == 0):
        for r in R:
            samples = r.get_samples_post_avg_tt(n_samples)
            sns.kdeplot(samples, fill=True)
        plt.title(f"Iterarion {i}", fontsize=20)
        plt.legend([f"route={idx}" for idx, _ in enumerate(R)], fontsize=16)
        plt.xlim(50, 200)
        plt.xlabel("Average Travel Time", fontsize=20)
        plt.ylabel("Density", fontsize=20)
        plt.show()
        plt.close()
