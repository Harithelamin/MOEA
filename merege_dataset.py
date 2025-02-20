import pandas as pd

# Load the datasets
stations_data = pd.read_csv("Datasets/california_stations.csv")
cost_data = pd.read_csv("Datasets/EV_tation_infrastructure_cost.csv")



# Cleaning/formatting the station data, ensuring power level is numeric
stations_data['Power Level (kW)'] = pd.to_numeric(stations_data['Power Level (kW)'], errors='coerce')

# Merge station data with cost data on 'Power Level (kW)'
merged_df = pd.merge(stations_data, cost_data, on='Power Level (kW)', how='left')

# Show the merged data with the calculated costs
print(merged_df[['Station Name', 'Address', 'Power Level (kW)', 'Chargers per Site', 
                 'Labor', 'Materials', 'Permit', 'Taxes', 'Total']])
# Remove the 'Type' column
merged_df = merged_df.drop(columns=['Type'])

# drop rows with missing values in the 'Total' column
merged_df = merged_df.dropna(subset=['Total'])

# Optionally, save the updated data to a new CSV file
merged_df.to_csv('Datasets/data.csv', index=False)
