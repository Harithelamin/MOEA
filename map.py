import os
import pandas as pd
import folium

def get_map():
    # Set file paths
    current_directory = os.getcwd()
    original_data_path = os.path.join(current_directory, "Datasets", "stations.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Create the save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Read CSV files
    stations_df = pd.read_csv(original_data_path)
    optimized_df = pd.read_csv(optimized_data_path)

    # Fixed map center: Downtown Los Angeles
    la_center = [34.0522, -118.2437]
    zoom_level = 14  # Adjusted for better city view

    # Create the map for both original and optimized stations
    combined_map = folium.Map(location=la_center, zoom_start=zoom_level)

    # Plot original stations (blue)
    for _, row in stations_df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7,
            popup="Original Station"
        ).add_to(combined_map)

    # Plot optimized stations (green)
    for _, row in optimized_df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.7,
            popup="Optimized Station"
        ).add_to(combined_map)

    # Save combined map
    combined_map_path = os.path.join(save_dir, "combined_stations_map_LA.html")
    combined_map.save(combined_map_path)

    print(f"Combined map saved to {combined_map_path}")

if __name__ == "__main__":
    get_map()
