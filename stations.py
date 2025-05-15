# Reference
# https://requests.readthedocs.io/en/latest/api/#requests.get
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
# https://openchargemap.org/site/develop/api

import os
import numpy as np
import requests
import pandas as pd
from geopy.distance import geodesic

# Parameters for the API request (focused on Los Angeles)
params = {
    "key": "65480684-8133-4ba5-9289-949cc656022d",
    "countrycode": "US",
    "latitude": 34.0522,      # Latitude for Los Angeles
    "longitude": -118.2437,   # Longitude for Los Angeles
    "distance": 30,           # 30 km radius around LA
    "distanceunit": "KM",
    "maxresults": 500,
    "compact": True,
    "verbose": False
}

def get_stations_data(url, file_path):
    output_dir = os.path.dirname(file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Prepare the stations list
        stations = []
        center_coords = (34.0522, -118.2437)  

        for station in data:
            address_info = station.get("AddressInfo", {})
            latitude = address_info.get("Latitude")
            longitude = address_info.get("Longitude")
            if latitude is None or longitude is None:
                continue

            station_coords = (latitude, longitude)
            if geodesic(center_coords, station_coords).km > 30:
                continue  # Skip stations outside the 30 km radius

            num_points = station.get("NumberOfPoints", "")
            connections = station.get("Connections", [])
            power_kw = next((conn.get("PowerKW", "") for conn in connections if conn.get("PowerKW")), "")

            stations.append([
                station.get("ID", ""),
                latitude,
                longitude,
                num_points,
                power_kw
            ])

        # Create a DataFrame
        df = pd.DataFrame(stations, columns=["station_id", "latitude", "longitude", "number_of_points", "power_kw"])
        df.replace("", np.nan, inplace=True)
        df.dropna(how='any', inplace=True)

        # Convert to numeric
        df['num_chargers'] = pd.to_numeric(df['number_of_points'], errors='coerce')
        df['charger_speed'] = pd.to_numeric(df['power_kw'], errors='coerce')

        df.drop(columns=['number_of_points', 'power_kw'], inplace=True)
        df = df.dropna()

        # Save to CSV
        df.to_csv(file_path, index=False)
        print(f"Los Angeles area station data successfully saved to {file_path}.")
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")

# Main testing function
def main():
    current_directory = os.getcwd()
    url = "https://api.openchargemap.io/v3/poi"
    data_path = os.path.join(current_directory, "Datasets", "stations.csv")
    get_stations_data(url, data_path)

if __name__ == "__main__":
    main()
