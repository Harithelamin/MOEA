# # Reference
# https://requests.readthedocs.io/en/latest/api/#requests.get
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
# https://openchargemap.org/site/develop/api
import os
import numpy as np
import requests
import pandas as pd

# The parameters for the API request
params = {
    "key": "65480684-8133-4ba5-9289-949cc656022d",
    "countrycode": "US",
    "state": "California", 
    "maxresults": 100,
    "compact": True,
    "verbose": False,
}

def get_stations_data(url, file_path):
    output_dir = os.path.dirname(file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        # prepare the stations list
        stations = [
            [
                station.get("ID", ""),
                station.get("AddressInfo", {}).get("Latitude", ""),
                station.get("AddressInfo", {}).get("Longitude", ""),
                station.get("NumberOfPoints", ""),
                next((conn.get("PowerKW", "") for conn in station.get("Connections", [])), "")
            ]
            for station in data if station.get("ID") and station.get("AddressInfo", {}).get("Latitude") and station.get("AddressInfo", {}).get("Longitude")
        ]

        # Create a DataFrame from the stations list
        df = pd.DataFrame(stations, columns=["station_id", "latitude", "longitude", "number_of_points", "power_kw"])

        # Drop rows with any missing data
        df.replace("", np.nan, inplace=True)
        df.dropna(how='any', inplace=True)

        # Convert 'number_of_points' and 'power_kw' to numeric values
        df['num_chargers'] = pd.to_numeric(df['number_of_points'], errors='coerce')
        df['charger_speed'] = pd.to_numeric(df['power_kw'], errors='coerce')

        df.drop(columns=['number_of_points'], inplace=True)
        df.drop(columns=['power_kw'], inplace=True)

        


        # Write to CSV
        df.to_csv(file_path, index=False)

        print(f"Data successfully saved to {file_path}.")
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")

# Testing
def main():
    current_directory = os.getcwd()
    url = "https://api.openchargemap.io/v3/poi"
    data_path = os.path.join(current_directory, "Datasets", "stations.csv")

    # Fetch and save the data
    get_stations_data(url, data_path)

if __name__ == "__main__":
    main()        


