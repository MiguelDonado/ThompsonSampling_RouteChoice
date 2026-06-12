import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from paths import CONVERGENCE_POST_MEANS, REGRET_PARQUET

true_means = (78.48, 80.13)
posterior_means = (78.32, 80.31)

plt.rcParams.update(
    {
        "font.size": 18,  # default text size
        "axes.titlesize": 22,  # title
        "axes.labelsize": 20,  # x/y labels
        "xtick.labelsize": 18,  # x tick labels
        "ytick.labelsize": 18,  # y tick labels
        "legend.fontsize": 18,
        "lines.linewidth": 2,
    }
)


def plot_convergence_post_mean_meantt(true_means, posterior_means):
    """
    Generates a plot that compares the true hidden avg rewards
    with the posterior means after convergence
    """
    path = CONVERGENCE_POST_MEANS

    plt.figure(figsize=(5, 5))

    plt.scatter(true_means, posterior_means)
    # Diagonal line y = x
    plt.plot([75, 85], [75, 85], color="k", alpha=0.5, linestyle="--")

    plt.xlim(75, 85)
    plt.ylim(75, 85)

    plt.xlabel("True Mean", fontsize=20)
    plt.ylabel("Posterior Mean", fontsize=20)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


# plot_convergence_post_mean_meantt(
#     true_means=true_means, posterior_means=posterior_means
# )

##############################
##############################
##############################


def plot_cumulative_route_selection_frequencies():
    """
    y-axis: Relative frequency
    x-axis: episode
    Put all routes in the same plot, one line per route
    It provides insight not only into how often each route is selected, but also into when those selections occur
    """
    freq_df = prepare_data_cumulative_route_selection_frequencies()

    for route, group in freq_df.groupby("route"):
        plt.plot(
            group["episode"],
            group["relative_frequency"],
            label=f"Route {route}",
        )

    plt.xlabel("Episode")
    plt.ylabel("Cumulative selection frequency")
    plt.title("Sioux Falls network\nCumulative route selection frequencies")
    plt.legend()
    plt.grid(True)

    plt.savefig(
        "/home/miguel/6.Projects/BayesianFinalProject/report/media/DefinitiveTS/Sioux_Falls_cumulative_RSF.pdf",
        bbox_inches="tight",
    )
    plt.savefig(
        "/home/miguel/6.Projects/BayesianFinalProject/report/media/DefinitiveTS/Sioux_Falls_cumulative_RSF.png",
        bbox_inches="tight",
        dpi=300,
    )

    plt.close()


def prepare_data_cumulative_route_selection_frequencies():
    df = pd.read_parquet(REGRET_PARQUET)
    routes = sorted(df["chosen_route"].unique())

    rows = []

    for episode in df["episode"]:
        history = df[df["episode"] <= episode]

        counts = history["chosen_route"].value_counts()

        for route in routes:
            # len(history): Number of episodes so far
            # counts.get(route,0): Number of times route was selected so far
            rel_freq = counts.get(route, 0) / len(history)

            rows.append(
                {
                    "episode": episode,
                    "route": route + 1,
                    "relative_frequency": rel_freq,
                }
            )

    freq_df = pd.DataFrame(rows)
    return freq_df


plot_cumulative_route_selection_frequencies()


def plot_cumulative_regret():
    df = pd.read_parquet(REGRET_PARQUET)

    plt.figure(figsize=(8, 5))

    plt.plot(
        df["episode"],
        df["cumulative_regret"],
    )

    plt.xlabel("Episode")
    plt.ylabel("Cumulative regret")
    plt.title("Toy network\nCumulative regret")

    plt.savefig(
        "/home/miguel/6.Projects/BayesianFinalProject/report/media/DefinitiveTS/Toy_cumulative_regret.pdf",
        bbox_inches="tight",
    )

    plt.savefig(
        "/home/miguel/6.Projects/BayesianFinalProject/report/media/DefinitiveTS/Toy_cumulative_regret.png",
        bbox_inches="tight",
        dpi=300,
    )

    plt.close()


# plot_cumulative_regret()


def plot_avg_regret():
    df = pd.read_parquet(REGRET_PARQUET)

    plt.figure(figsize=(8, 5))

    df["average_regret"] = df["cumulative_regret"] / df["episode"]

    plt.plot(
        df["episode"],
        df["average_regret"],
    )

    plt.xlabel("Episode")
    plt.ylabel("Average regret")
    plt.title("Sioux Falls network\nAverage regret per episode")

    plt.savefig(
        "/home/miguel/6.Projects/BayesianFinalProject/report/media/DefinitiveTS/Sioux_Falls_avg_regret.pdf",
        bbox_inches="tight",
    )

    plt.savefig(
        "/home/miguel/6.Projects/BayesianFinalProject/report/media/DefinitiveTS/Sioux_Falls_avg_regret.png",
        bbox_inches="tight",
        dpi=300,
    )

    plt.close()


# plot_avg_regret()
