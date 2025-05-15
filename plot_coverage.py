import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_EVCS_Coverage(save_dir, original_data_path, optimized_data_path):
    # Load datasets
    original_data = pd.read_csv(original_data_path)
    optimized_data = pd.read_csv(optimized_data_path)
    
    # Select coverage column
    original_coverage = original_data['coverage']
    optimized_coverage = optimized_data['coverage']
    
    # Get num of stations
    original_station_count = range(1, len(original_data) + 1)
    optimized_station_count = range(1, len(optimized_data) + 1)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(original_station_count, original_coverage, label='Original Coverage', color='b', marker='o')
    plt.plot(optimized_station_count, optimized_coverage, label='Optimized Coverage', color='g', marker='x')
    plt.xlabel('Number of Stations')
    plt.ylabel('Coverage')
    plt.title('Coverage Per Stations')
    plt.legend()
    
    # Save the plot
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, "coverage_stations.png"))
    plt.show()

def main():
    # Fle paths
    current_directory = os.getcwd()
    original_data_path = os.path.join(current_directory, "Datasets", "stations_with_avg_distance.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_avg_distance.csv")
    save_dir = os.path.join(current_directory, "Fig")
    
    # Call the function
    plot_EVCS_Coverage(save_dir, original_data_path, optimized_data_path)

if __name__ == "__main__":
    main()
