import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_results(save_dir, optimized_data_path):
    # Load the optimized data
    data = pd.read_csv(optimized_data_path)
    
    coverage_values = data['coverage']
    charger_speed_values = data['charger_speed']
    avg_distance_values = data['average_vehicle_distance_km']

    # Scatter plot
    plt.figure(figsize=(8, 5))
    scatter = plt.scatter(coverage_values, charger_speed_values, 
                          c=avg_distance_values, cmap='coolwarm', s=50)
    plt.colorbar(scatter, label='Avg EV Distance (km)')
    plt.title('Coverage vs Charger Speed (colored by Avg EV Distance)')
    plt.xlabel('Coverage (km)')
    plt.ylabel('Charger Speed (kW)')
    plt.grid(True)

    # Save the plot
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "results.png")
    plt.savefig(save_path)
    plt.show()
    print(f"Plot saved to {save_path}")

def main():
    # Paths
    current_directory = os.getcwd()
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_avg_distance.csv")
    save_dir = os.path.join(current_directory, "Fig")
    
    # plot function
    plot_results(save_dir, optimized_data_path)

if __name__ == "__main__":
    main()
