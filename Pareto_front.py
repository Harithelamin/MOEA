import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Define the objectives problem 
# 1. Maximize coverage
# 2. Maximize charger speed to reduce waiting time
# 3. Minimize stations num
# 4. Minimize chargers num
# 5. Minimize avarage distance

def plot_pareto_front(pareto_df, save_dir):
    pareto_df['num_stations'] = pareto_df.apply(lambda row: len(str(row['station_id']).split(',')), axis=1)

    # Extract columns
    num_stations = pareto_df["num_stations"]
    num_chargers = pareto_df["num_chargers"]
    coverage = pareto_df["coverage"]
    charger_speed = pareto_df["charger_speed"]
    avg_vehicle_distance = pareto_df["average_vehicle_distance_km"]

    # We need to normalize average distance
    min_size = 30
    max_size = 200
    distance_norm = (avg_vehicle_distance - avg_vehicle_distance.min()) / (avg_vehicle_distance.max() - avg_vehicle_distance.min())
    # we need it in the scatter
    marker_sizes = max_size - (distance_norm * (max_size - min_size)) 

    # Create 3D plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # num_stations
    scatter = ax.scatter(
        coverage, charger_speed, num_chargers,
        c=num_stations, cmap='viridis', s=60, alpha=0.8, s=marker_sizes
    )

    ax.set_xlabel('Coverage (maximize)')
    ax.set_ylabel('Charger Speed (maximize)')
    ax.set_zlabel('Number of Chargers (minimize)')
    ax.set_title('Pareto Front')

    #add the number of staions 
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Number of Stations (minimize)')

    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)
    # Save plot
    plot_path = os.path.join(save_dir, "Pareto_Front.png")
    plt.savefig(plot_path)
    plt.close()


def main():
    current_directory = os.getcwd()
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_covarage.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load the optimized data
    pareto_front = pd.read_csv(optimized_data_path)

    # Plot and save the Pareto front visualization
    plot_pareto_front(pareto_front, save_dir)


if __name__ == "__main__":
    main()
