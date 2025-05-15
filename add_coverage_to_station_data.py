import math
from geopy.distance import geodesic
import pandas as pd
import os

# Calculate coverage area based on geodesic distance
def calculate_coverage(data, radius_km=5):
    coverage_list = []

    # For each station, count how many other stations are within the coverage radius
    for i in range(len(data)):
        station = (data['latitude'][i], data['longitude'][i])
        count_within_radius = 0
        
        for j in range(len(data)):
            if i != j:
                other_station = (data['latitude'][j], data['longitude'][j])
                # Calculate the distance between the stations
                distance = geodesic(station, other_station).km
                if distance <= radius_km:
                    count_within_radius += 1
        
        # Store the number of stations within the radius for this station
        coverage_list.append(count_within_radius)
        
    return coverage_list

# Add coverage columns in dataset  
def add_coverage(data_path, new_data_path):
    data = pd.read_csv(data_path)

    # Ensure numeric columns
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    # Clean and reset index
    data.dropna(subset=['latitude', 'longitude'], inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Compute individual coverage
    data['coverage'] = calculate_coverage(data, radius_km=5)

    # Save to new CSV
    data.to_csv(new_data_path, index=False)
    print(f"Saved data to: {new_data_path}")

# Testing
def main():
    # Define data path
    current_directory = os.getcwd()
    data_path = os.path.join(current_directory, "Datasets", "stations.csv")
    new_data_path = os.path.join(current_directory, "Datasets", "stations_with_coverage.csv")

    # Calculate coverage
    add_coverage(data_path, new_data_path)

if __name__ == "__main__":
    main()
