import os
import pandas as pd

# Charger cost calculation
def calculate_charger_cost(row):
    if pd.notna(row['power_kw']):
        power_kw = row['power_kw']
        
        # Define cost ranges
        if 3 <= power_kw < 7:
            # Level 1 or Level 2 Charger
            hardware_cost = (500 + 1500) / 2  
            installation_cost = (300 + 500) / 2  
        elif 7 <= power_kw < 26:
            # Level 2 Charger
            hardware_cost = (1500 + 5000) / 2  
            installation_cost = (1000 + 2500) / 2  
        elif 50 <= power_kw < 100:
            # DC Fast Charger (50 kW - 100 kW)
            hardware_cost = (30000 + 50000) / 2  
            installation_cost = (50000 + 100000) / 2 
        elif 100 <= power_kw < 150:
            # DC Fast Charger (100 kW - 150 kW)
            hardware_cost = (80000 + 150000) / 2  
            installation_cost = (50000 + 100000) / 2  
        elif 150 <= power_kw < 200:
            # DC Fast Charger (150 kW - 200 kW)
            hardware_cost = (100000 + 170000) / 2 
            installation_cost = (100000 + 150000) / 2  
        elif 200 <= power_kw < 350:
            # Charger (200 kW - 350 kW)
            hardware_cost = (100000 + 150000) / 2  
            installation_cost = (150000 + 250000) / 2  
        elif 350 <= power_kw <= 400:
            # Charger (350 kW - 400 kW)
            hardware_cost = (120000 + 150000) / 2  
            installation_cost = (150000 + 250000) / 2  
        else:
            return None
        
        # Return total cost (hardware cost + installation cost)
        total_cost = hardware_cost + installation_cost
        return total_cost
    else:
        return None 

# calculate station cost
def calculate_station_cost(station_data):
    if 'charger_cost' in station_data.columns and 'number_of_points' in station_data.columns:
        # Calculate station cost
        station_data['station_cost'] = station_data['charger_cost'] * station_data['number_of_points']
    else:
        return None
    return station_data

# Load data from CSV
def load_data_from_csv(station_data_path):
    return pd.read_csv(station_data_path)

# run calculatin process
def calculatin_process(station_data_path):
    current_directory = os.getcwd()
    # Load the data
    station_data = load_data_from_csv(station_data_path)

    # Calculate charger cost
    station_data['charger_cost'] = station_data.apply(calculate_charger_cost, axis=1)

    # Calculate station cost
    station_data = calculate_station_cost(station_data)

    # Save the file
    output_path = os.path.join(current_directory, "Datasets", "station_cost.csv")
    station_data.to_csv(output_path, index=False)
      
    print(f"Costs file saved")


# Testing
def main():
    current_directory = os.getcwd()
    station_data_path = os.path.join(current_directory, "Datasets", "stations.csv")
    calculatin_process(station_data_path)
    


if __name__ == "__main__":
    main()
