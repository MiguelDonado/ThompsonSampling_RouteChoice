import matplotlib.pyplot as plt


def plot_histogram_tt(tt, bins):
    plt.hist(tt, bins=bins)

    plt.xlabel("Agent travel time")
    plt.ylabel("Frequency")
    plt.title("Route travel time distribution")

    plt.show()
