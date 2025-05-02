import os
import pandas as pd
import folium

# plot station locations on map
def plot_station_locations(data, save_dir, file_name):
    # latitude and longitude
    latitude = data["latitude"]
    longitude = data["longitude"]
    station_ids = data["station_id"]

    # folium map of the latitudes and longitudes
    m = folium.Map(location=[latitude.mean(), longitude.mean()], zoom_start=5)

    # Add each station on the map
    for idx, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Station ID: {row['station_id']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    os.makedirs(save_dir, exist_ok=True)

    # Save the map as an HTML file
    map_path = os.path.join(save_dir, file_name + ".html")
    m.save(map_path)
    print(f"Map saved at {map_path}")


# Get Original map
def get_original_map():
    current_directory = os.getcwd()
    original_data_path = os.path.join(current_directory, "Datasets", "stations_with_covarage.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_covarage.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load the original data
    data = pd.read_csv(original_data_path)

    # Plot and save the station locations
    plot_station_locations(data, save_dir, "original_map")

# Get Original map
def get_optimized_map():
    current_directory = os.getcwd()
    original_data_path = os.path.join(current_directory, "Datasets", "stations_with_covarage.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_covarage.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load the original data
    data = pd.read_csv(optimized_data_path)

    # Plot and save the station locations
    plot_station_locations(data, save_dir, "optimized_map")


# Main function
def main():
    get_original_map()
    get_optimized_map()


if __name__ == "__main__":
    main()
