import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(file_path):
    """
    Load the data from a CSV file.
    """
    df = pd.read_csv(file_path)
    return df


if __name__ == "__main__":
    rapf_data = load_data("results_1k.csv")
    bapf_data = load_data("results_BAPF.csv")

    # generate mean and std for each column
    rapf_mean = rapf_data.mean()
    rapf_std = rapf_data.std()
    rapf_min = rapf_data.min()
    rapf_max = rapf_data.max()
    rapf_median = rapf_data.median()
    
    bapf_mean = bapf_data.mean()
    bapf_std = bapf_data.std()
    bapf_min = bapf_data.min()
    bapf_max = bapf_data.max()
    bapf_median = bapf_data.median()

    obstacle_densities = [75,125,175,225,275]

    plt.plot(
        obstacle_densities,
        rapf_mean,
        label="RAPF Mean",
        marker="x",
    )
    plt.title("Average minimum communication distance - RAPF-T")
    plt.xlabel("Obstacle Densities")
    plt.ylabel("Values")
    plt.savefig("rapf_mean.png")
    plt.clf()

    plt.plot(
        obstacle_densities,
        bapf_mean,
        label="BAPF Mean",
        marker="x",
    )
    plt.title("Average minimum communication distance - BAPF")
    plt.xlabel("Obstacle Densities")
    plt.ylabel("Values")
    plt.savefig("bapf_mean.png")
    plt.clf()


    # Plot for RAPF
    plt.figure(figsize=(10, 6))
    for percentile in [75, 90, 99]:
        rapf_percentile = rapf_data.quantile(percentile / 100.0)
        plt.fill_between(
            obstacle_densities,
            rapf_mean,
            rapf_percentile,
            alpha=0.2,
            label=f"RAPF {percentile}th Percentile",
        )
    plt.plot(obstacle_densities, rapf_mean, label="RAPF Mean", marker="x")
    plt.title("Percentile Bounds for RAPF")
    plt.xlabel("Obstacle Densities")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.savefig("rapf_percentile_bounds.png")
    plt.close()

    # Plot for BAPF
    plt.figure(figsize=(10, 6))
    for percentile in [75, 90, 99]:
        bapf_percentile = bapf_data.quantile(percentile / 100.0)
        plt.fill_between(
            obstacle_densities,
            bapf_mean,
            bapf_percentile,
            alpha=0.2,
            label=f"BAPF {percentile}th Percentile",
        )
    plt.plot(obstacle_densities, bapf_mean, label="BAPF Mean", marker="x")
    plt.title("Percentile Bounds for BAPF")
    plt.xlabel("Obstacle Densities")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.savefig("bapf_percentile_bounds.png")
    plt.close()
