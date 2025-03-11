import pandas as pd

# Load the datasets
stations_data = pd.read_csv("Datasets/california_stations.csv")
cost_data = pd.read_csv("Datasets/EV_tation_infrastructure_cost.csv")

def merege_data():
       # Cleaning/formatting the station data, ensuring power level is numeric
       stations_data['Power Level (kW)'] = pd.to_numeric(stations_data['Power Level (kW)'], errors='coerce')

       # Merge station data with cost data on 'Power Level (kW)'
       merged_data = pd.merge(stations_data, cost_data, on='Power Level (kW)', how='left')

       # Merged data with the calculated costs
       print(merged_data[['Station Name', 'Address', 'Power Level (kW)', 'Chargers per Site', 
                 'Labor', 'Materials', 'Permit', 'Taxes', 'Total']])
       # Remove the 'Type' column
       merged_data = merged_data.drop(columns=['Type'])

       # Drop the specified columns Labor, Materials, Permit, Taxes
       merged_data = merged_data.drop(columns=['Labor', 'Materials', 'Permit', 'Taxes'])

       # drop rows with missing values in the 'Total' column
       merged_data = merged_data.dropna(subset=['Total'])

       # Save the updated data to a new CSV file
       merged_data.to_csv('Datasets/data.csv', index=False)

# Testing
def main():
    print("start")

if __name__=="__main__":
    main()
    merege_data()