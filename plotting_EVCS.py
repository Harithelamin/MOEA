# pip3 install folium
import os
import folium
import pandas as pd

# Load the data
data = pd.read_csv('Datasets/data.csv')

def ploatin_EVCS():
    # Print out the column names in dataset
    print("Columns in dataset:", data.columns)

    # Remove any leading/trailing whitespace from column names
    data.columns = data.columns.str.strip()

    # Split the Coordinates into Latitude and Longitude
    data[['Latitude', 'Longitude']] = data['Coordinates'].str.split(', ', expand=True)

    # Convert Latitude and Longitude to numeric values
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')

    # Create a base map centered around California
    m = folium.Map(location=[36.7783, -119.4179], zoom_start=6)

    # Define the path of charger icon image
    # From https://www.flaticon.com/free-icons/charger
    charger_icon_path = os.path.join('Images', 'EV_Charging_Station_Icon.png') 


    # Plot each EV station on the map
    for index, row in data.iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"Station: {row['Station Name']}\nAddress: {row['Address']}\nCharging Type: {row['Charging Type']}\nPower Level: {row['Power Level (kW)']}\nChargers: {row['Chargers per Site']}\nTotal: {row['Total']}",
            icon=folium.CustomIcon(icon_image=charger_icon_path, icon_size=(10, 10)),
            ).add_to(m)

    # Save the map as an HTML file
    m.save("evcs_map.html")
    print("Map has been saved as 'evcs_map.html'")
