import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_distance(original_data, optimized_data, save_dir):
    plt.figure(figsize=(8,6))

    # Plot original EVCS
    plt.scatter(original_data['coverage'], original_data['average_vehicle_distance_km'],
                c='blue', label='Original EVSC Network', alpha=0.7, edgecolors='k', s=80)

    # Plot optimized EVSC 
    plt.scatter(optimized_data['coverage'], optimized_data['average_vehicle_distance_km'],
                c='red', label='Optimized EVSC Network', alpha=0.7, edgecolors='k', s=80)

    plt.xlabel('Coverage (maximize)')
    plt.ylabel('Average EV Distance (minimize)')
    plt.title('Comparison: Coverage vs Average Vehicle Distance')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)

    # Save the plot
    plot_path = os.path.join(save_dir, "distance.png")
    plt.savefig(plot_path)
    plt.close()

def main():
    current_directory = os.getcwd()
    original_data_path = os.path.join(current_directory, "Datasets", "stations_with_avg_distance.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_covarage.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load data
    original_data = pd.read_csv(original_data_path)
    optimized_data = pd.read_csv(optimized_data_path)

    # Plot dsitances
    plot_distance(original_data, optimized_data, save_dir)

if __name__ == "__main__":
    main()
