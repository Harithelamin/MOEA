import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

def plot_pareto_front(pareto_df, save_dir):
    pareto_df['num_stations'] = pareto_df['station_id'].apply(lambda x: len(str(x).split(',')))

    coverage = pareto_df["coverage"]
    charger_speed = pareto_df["charger_speed"]
    num_chargers = pareto_df["num_chargers"]
    num_stations = pareto_df["num_stations"]
    avg_distance = pareto_df["average_vehicle_distance_km"]

    min_marker_size = 30
    max_marker_size = 200
    distance_norm = (avg_distance - avg_distance.min()) / (avg_distance.max() - avg_distance.min())
    marker_sizes = max_marker_size - (distance_norm * (max_marker_size - min_marker_size))

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(
        coverage, 
        charger_speed, 
        num_chargers,
        c=num_stations,
        cmap='viridis',
        s=marker_sizes,
        alpha=0.8,
        edgecolors='k',
        vmin=1,
        vmax=20
    )

    ax.set_xlabel('Coverage (maximize)')
    ax.set_ylabel('Charger Speed (maximize)')
    ax.set_zlabel('Number of Chargers (minimize)')
    ax.set_title('Pareto Front of EVCS Optimization')

    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Number of Stations (minimize)')
    cbar.set_ticks(range(1, 21))  # Optional for clearer ticks on colorbar

    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)
    plot_path = os.path.join(save_dir, "Pareto_Front.png")
    plt.savefig(plot_path)
    plt.close()

def main():
    current_directory = os.getcwd()
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_avg_distance.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load the Pareto front data from CSV
    pareto_front = pd.read_csv(optimized_data_path)

    # Plot and save the Pareto front visualization
    plot_pareto_front(pareto_front, save_dir)

if __name__ == "__main__":
    main()
