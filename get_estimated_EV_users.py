import os
import pandas as pd
from geopy.distance import geodesic

# Function to calculate the distance between two points
def get_distance_to_station(station_lat, station_lon, vehicle_lat, vehicle_lon):
    return geodesic((station_lat, station_lon), (vehicle_lat, vehicle_lon)).km

def get_station_data_with_estimated_ev_count(station_path, vehicle_path, output_path, ZIP_code_tabulation_areas_path):
    # Load data
    stations = pd.read_csv(station_path)
    vehicles = pd.read_csv(vehicle_path)
    zcta = pd.read_csv(ZIP_code_tabulation_areas_path)

    # Debug: Check the column names in ZCTA data
    print("ZCTA Data Columns (before renaming):", zcta.columns)

    # Prepare ZIP centroid data (renaming the columns correctly)
    zcta = zcta.rename(columns={
        'Zip Code Tabulation Area Code': 'ZIP',  # Correct column name for ZIP code
        'Centroid Latitude': 'latitude',
        'Centroid Longitude': 'longitude'
    })

    # Debug: Check column names after renaming
    print("ZCTA Data Columns (after renaming):", zcta.columns)

    zcta['ZIP'] = zcta['ZIP'].astype(str)
    zcta_coords = zcta[['latitude', 'longitude']]

    # Ensure vehicles dataframe has the correct 'ZIP' column
    vehicles = vehicles.rename(columns={'ZIP Code': 'ZIP'})
    vehicles['ZIP'] = vehicles['ZIP'].astype(str)
    
    # Sum vehicles per ZIP code
    ev_counts = vehicles.groupby('ZIP')['Vehicles'].sum().to_dict()

    # Prepare Station Coordinates
    stations_coords = stations[['station_id', 'latitude', 'longitude']]

    # Initialize a list to store EV counts for each station
    stations['Vehicle_Count'] = 0

    # Calculate distance between stations and ZCTA centroids, then sum EVs
    for _, station in stations.iterrows():
        station_lat = station['latitude']
        station_lon = station['longitude']
        
        # Calculate the nearest ZCTA by distance
        distances = zcta.apply(
            lambda row: get_distance_to_station(station_lat, station_lon, row['latitude'], row['longitude']),
            axis=1
        )

        # Find the nearest ZIPs within 10 km
        nearby_zips = zcta[distances <= 10]['ZIP'].values

        # Sum the EV counts for these nearby ZIPs
        total_ev_count = sum(ev_counts.get(zip_code, 0) for zip_code in nearby_zips)

        # Update the station's EV count
        stations.loc[stations['station_id'] == station['station_id'], 'Vehicle_Count'] = total_ev_count

    # Save the output with the EV count
    stations.to_csv(output_path, index=False)
    print(stations[['station_id', 'latitude', 'longitude', 'Vehicle_Count']])

# Main function
def main():
    current_directory = os.getcwd()
    station_data_path = os.path.join(current_directory, "Datasets", "stations_with_covarage.csv")
    EV_Registration_data_path = os.path.join(current_directory, "Datasets", "vehicle-fuel-type-count-by-zip-code-20231.csv")
    ZIP_code_tabulation_areas_path = os.path.join(current_directory, "Datasets", "Census_ZIP_Code_Tabulation_Areas_2010_v1_-2956920033234507074.csv")
    output_path = os.path.join(current_directory, "Datasets", "station_data_with_estimated_ev_count.csv")

    get_station_data_with_estimated_ev_count(station_data_path, EV_Registration_data_path, ZIP_code_tabulation_areas_path, output_path)

if __name__ == "__main__":
    main()
