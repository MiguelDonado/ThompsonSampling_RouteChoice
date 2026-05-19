import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew
import seaborn as sns
import matplotlib.pyplot as plt
from paths import POST_AVG_TT_DIR
from config import config


def plot_histogram_and_kde_tt(tt, path, idx_route):
    mean = np.mean(tt)
    std = np.std(tt)

    # Skewness
    skewness = skew(tt)

    # Quantiles
    q50 = np.percentile(tt, 50)
    q90 = np.percentile(tt, 90)
    q95 = np.percentile(tt, 95)

    sns.histplot(tt, bins="fd", stat="density", kde=True)

    # Legend entries only
    plt.plot([], [], " ", label=f"Mean = {mean:.2f}")
    plt.plot([], [], " ", label=f"Std = {std:.2f}")
    plt.plot([], [], " ", label=f"Skew = {skewness:.2f}")

    plt.plot([], [], " ", label=f"Q50 = {q50:.2f}")
    plt.plot([], [], " ", label=f"Q90 = {q90:.2f}")
    plt.plot([], [], " ", label=f"Q95 = {q95:.2f}")

    plt.xlabel("Travel time")
    plt.ylabel("Density")
    plt.title(
        f"Route {idx_route} travel time distribution\n"
        f"(Monte Carlo approximation using {config.n_episodes} simulations"
    )
    plt.legend()

    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def draw_distributions(R, i, n_samples):
    if i < 10 or (i < 100 and (i + 1) % 10 == 0) or ((i + 1) % 100 == 0):
        path = POST_AVG_TT_DIR / config.name_network / f"post_avg_tt_{i}.png"
        for r in R:
            samples = r.get_samples_post_avg_tt(n_samples)
            sns.kdeplot(samples, fill=True)
        plt.title(f"Iterarion {i}\n" "Posteriors mean travel time", fontsize=20)
        plt.legend([f"true_mean_tt={r.true_mean_tt}" for r in R], fontsize=16)
        plt.xlim(50, 200)
        plt.xlabel("Average Travel Time", fontsize=20)
        plt.ylabel("Density", fontsize=20)
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
