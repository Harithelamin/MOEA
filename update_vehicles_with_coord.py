
# Merge the datasets based on the Zip column
# Filter vehicles where Fuel is 'Battery Electric'
# Remove rows with missing values
# Filter vehicles for Los angles

import os
import pandas as pd
from geopy.distance import geodesic

# Los Angeles, CA Area
CENTER_COORDINATES = (34.0522, -118.2437)  
RADIUS_KM = 30        


def update_vehicle_data_with_coordinates(EV_Registration_data_path, ZIP_code_tabulation_areas_path, vehice_data_with_coordinates):
    # Load data
    vehicles = pd.read_csv(EV_Registration_data_path)
    zcta = pd.read_csv(ZIP_code_tabulation_areas_path)

   
    # Rename Zip code, latitude, longitude columns in the ZCTA data
    zcta = zcta.rename(columns={
        'Zip Code Tabulation Area Code': 'ZIP', 
        'Centroid Latitude': 'latitude', 
        'Centroid Longitude': 'longitude'
    })
    
    # Ensure the ZIP column in both datasets is string format
    vehicles['ZIP Code'] = vehicles['ZIP Code'].astype(str)
    zcta['ZIP'] = zcta['ZIP'].astype(str)

    # Filter vehicles where Fuel is 'Battery Electric'
    filtered_vehicles = vehicles[vehicles['Fuel'] == 'Battery Electric']

    
    # Merge the datasets based on the Zip column
    updated_vehicles = filtered_vehicles.merge(zcta[['ZIP', 'latitude', 'longitude']], left_on='ZIP Code', right_on='ZIP', how='left')
    
    # Remove rows with missing values
    updated_vehicles = updated_vehicles.dropna()

    
    # Filter vehicles for Los angles
    #print(updated_vehicles.columns)
    updated_vehicles = updated_vehicles[updated_vehicles.apply(lambda row: geodesic(CENTER_COORDINATES, (row['latitude'], row['longitude'])).km <= 30, axis=1)]



    # Save the dataset
    updated_vehicles.to_csv(vehice_data_with_coordinates, index=False)
   
# Main function
def main():
    current_directory = os.getcwd()
    EV_Registration_data_path = os.path.join(current_directory, "Datasets", "vehicle-fuel-type-count-by-zip-code-20231.csv")
    ZIP_code_tabulation_areas_path = os.path.join(current_directory, "Datasets", "Census_ZIP_Code_Tabulation_Areas_2010_v1_-2956920033234507074.csv")
    vehice_data_with_coordinates = os.path.join(current_directory, "Datasets", "vehice_data_with_coordinates.csv")

    update_vehicle_data_with_coordinates(EV_Registration_data_path, ZIP_code_tabulation_areas_path, vehice_data_with_coordinates)
    #print_lat_lon_area(vehice_data_with_coordinates)
if __name__ == "__main__":
    main()
