import os
import pandas as pd
from geopy.distance import geodesic


def update_vehicle_data_with_coordinates(EV_Registration_data_path, ZIP_code_tabulation_areas_path, vehice_data_with_coordinates):
    # Load data
    vehicles = pd.read_csv(EV_Registration_data_path)
    zcta = pd.read_csv(ZIP_code_tabulation_areas_path)

   
# Main function
def main():
    current_directory = os.getcwd()
    EV_Registration_data_path = os.path.join(current_directory, "Datasets", "vehicle-fuel-type-count-by-zip-code-20231.csv")
    ZIP_code_tabulation_areas_path = os.path.join(current_directory, "Datasets", "Census_ZIP_Code_Tabulation_Areas_2010_v1_-2956920033234507074.csv")
    vehice_data_with_coordinates = os.path.join(current_directory, "Datasets", "vehice_data_with_coordinates.csv")

    update_vehicle_data_with_coordinates(EV_Registration_data_path, ZIP_code_tabulation_areas_path, vehice_data_with_coordinates)

if __name__ == "__main__":
    main()
