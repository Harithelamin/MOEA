import os
import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def compute_average_distance_per_station(station_data_path, vehicle_data_path, output_path):
    # Load datasets
    stations = pd.read_csv(station_data_path)
    vehicles = pd.read_csv(vehicle_data_path)

    # Drop rows with missing coordinates
    vehicles = vehicles.dropna(subset=['latitude', 'longitude']).copy()
    stations = stations.dropna(subset=['latitude', 'longitude']).copy()

    # Convert to float
    vehicles[['latitude', 'longitude']] = vehicles[['latitude', 'longitude']].astype(float)
    stations[['latitude', 'longitude']] = stations[['latitude', 'longitude']].astype(float)

    avg_distances = []

    for _, station in stations.iterrows():
        lat_s, lon_s = station['latitude'], station['longitude']
        lat_v = vehicles['latitude'].values
        lon_v = vehicles['longitude'].values

        distances = haversine(lat_s, lon_s, lat_v, lon_v)
        avg_distance = np.mean(distances)
        avg_distances.append(avg_distance)

    stations['average_vehicle_distance_km'] = avg_distances
    stations.to_csv(output_path, index=False)
    print(f"✅ Updated station file saved at: {output_path}")

def main():
    current_directory = os.getcwd()
    station_data_path = os.path.join(current_directory, "Datasets", "stations_with_covarage.csv")
    vehicle_data_path = os.path.join(current_directory, "Datasets", "vehice_data_with_coordinates.csv")
    output_path = os.path.join(current_directory, "Datasets", "stations_with_avg_distance.csv")

    compute_average_distance_per_station(station_data_path, vehicle_data_path, output_path)

if __name__ == "__main__":
    main()
