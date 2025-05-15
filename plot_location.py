import os
from matplotlib import pyplot as plt
import pandas as pd

# Plot station locations on map
def plot_station_locations(data, save_dir, file_name):
    # Latitude and longitude
    latitude = data["latitude"]
    longitude = data["longitude"]

    # Create a scatter plot for both original and optimized data
    plt.scatter(longitude, latitude, color='blue', label='Station Locations', marker='o')
    
    # Adding labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('EVCS Locations')
    plt.legend()

    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Save the plot as a PNG file
    plt.savefig(os.path.join(save_dir, file_name + ".png"))

    # Close the plot to avoid it being displayed multiple times
    plt.close()


# Get Original map
def get_original_map():
    current_directory = os.getcwd()
    original_data_path = os.path.join(current_directory, "Datasets", "stations.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load the original data
    data = pd.read_csv(original_data_path)

    # Plot and save the station locations
    plot_station_locations(data, save_dir, "original_map")


# Get Optimized map
def get_optimized_map():
    current_directory = os.getcwd()
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load the optimized data
    data = pd.read_csv(optimized_data_path)

    # Plot and save the station locations
    plot_station_locations(data, save_dir, "optimized_map")


# Main function
def main():
    get_original_map()
    get_optimized_map()


if __name__ == "__main__":
    main()
