import matplotlib.pyplot as plt
import numpy as np


def plot_histogram_tt(tt, bins):
    mean = np.mean(tt)
    std = np.std(tt)

    plt.hist(tt, bins=bins)

    # Legend entries only
    plt.plot([], [], " ", label=f"Mean = {mean:.2f}")
    plt.plot([], [], " ", label=f"Std = {std:.2f}")

    plt.xlabel("Agent travel time")
    plt.ylabel("Frequency")
    plt.title("Route travel time distribution")

    plt.legend()

    plt.show()
