import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_ev_distance_and_station_count(save_dir, original_path, optimized_path):
    # Load datasets
    original = pd.read_csv(original_path)
    optimized = pd.read_csv(optimized_path)

    # Extract metrics
    labels = ['EVCS Network', 'Optimized EVCS Network']
    avg_distances = [
        original['average_vehicle_distance_km'].mean(),
        optimized['average_vehicle_distance_km'].mean()
    ]
    station_counts = [len(original), len(optimized)]

    # Bar
    x = np.arange(len(labels))
    width = 0.35

    # Plot setup
    plt.figure(figsize=(8, 5))
    bar1 = plt.bar(x - width/2, avg_distances, width, label='Avg Distance (km)', color='skyblue')
    bar2 = plt.bar(x + width/2, station_counts, width, label='Number of Stations', color='orange')

    # Add labels
    plt.ylabel('Values')
    plt.title('EV Distance With Nearest EVCS')
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)

    # Annotate values
    for bar in bar1 + bar2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{height:.1f}', ha='center', va='bottom')

    # Save and show plot
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "ev_distance.png")
    plt.savefig(save_path)
    plt.show()
    print(f"Plot saved to {save_path}")

def main():
    current_dir = os.getcwd()
    original_path = os.path.join(current_dir, "Datasets", "stations_with_avg_distance.csv")
    optimized_path = os.path.join(current_dir, "Datasets", "optimized_data_with_avg_distance.csv")
    save_dir = os.path.join(current_dir, "Fig")

    plot_ev_distance_and_station_count(save_dir, original_path, optimized_path)

if __name__ == "__main__":
    main()
