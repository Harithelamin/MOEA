# Reference
# Official documentation for Matplotlib, which is used for creating plots.
# Link: https://matplotlib.org/stable/contents.html
import os
import sys
import folium
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
import seaborn  as sns


import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.pyplot as plt
import seaborn as sns

def plot_objective(pareto_front, output_directory):
    # Number of stations
    num_stations = len(pareto_front)

    # Create figure for all subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Locations
    sns.scatterplot(x='longitude', y='latitude', data=pareto_front, ax=axes[0, 0])
    axes[0, 0].set_title("Station Locations")
    axes[0, 0].set_xlabel("Longitude")
    axes[0, 0].set_ylabel("Latitude")

    # Display the number of stations 
    axes[0, 0].text(0.5, 0.05, f"Total Stations: {num_stations}", horizontalalignment='center', 
                    verticalalignment='center', transform=axes[0, 0].transAxes, fontsize=12, color='black', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))  # Adjust bbox

    # Plot 2: Charger Speed
    sns.histplot(pareto_front['charger_speed'], kde=True, ax=axes[0, 1])
    axes[0, 1].set_title("Charger Speed Distribution")
    axes[0, 1].set_xlabel("Charger Speed (kW)")
    axes[0, 1].set_ylabel("Frequency")

    # Plot 3: Number of Chargers per Station
    sns.barplot(x='station_id', y='num_chargers', data=pareto_front, ax=axes[1, 0])
    axes[1, 0].set_title("Number of Chargers per Station")
    axes[1, 0].set_xlabel("Station ID")
    axes[1, 0].set_ylabel("Number of Chargers")

    # Plot 4: Charger Speed vs Chargers Number
    sns.scatterplot(x='num_chargers', y='charger_speed', data=pareto_front, ax=axes[1, 1])
    axes[1, 1].set_title("Charger Speed vs Number of Chargers")
    axes[1, 1].set_xlabel("Number of Chargers")
    axes[1, 1].set_ylabel("Charger Speed (kW)")

    # Adjust layout
    plt.tight_layout()

    # Save the combined figure
    fig.savefig(f'{output_directory}/all_plots.png')  # Saving as one figure
    plt.clf()

    # Optionally, save individual plots after adjusting layout for clarity
    sns.scatterplot(x='longitude', y='latitude', data=pareto_front).set(title="Station Locations")
    plt.savefig(f'{output_directory}/station_locations.png')
    plt.clf()

    sns.histplot(pareto_front['charger_speed'], kde=True).set(title="Charger Speed Distribution")
    plt.savefig(f'{output_directory}/charger_speed.png')
    plt.clf()

    sns.barplot(x='station_id', y='num_chargers', data=pareto_front).set(title="Number of Chargers per Station")
    plt.savefig(f'{output_directory}/num_chargers_per_station.png')
    plt.clf()

    sns.scatterplot(x='num_chargers', y='charger_speed', data=pareto_front).set(title="Charger Speed vs Number of Chargers")
    plt.savefig(f'{output_directory}/charger_speed_vs_num_chargers.png')
    plt.clf()

    print("Plots saved successfully.")




########################################



def plot_convergence(pareto_front, output_file):

    plt.scatter(pareto_front['latitude'], pareto_front['longitude'], color='blue')

    # Set labels and title for the plot
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Convergence Plot')

    # Save the plot to the specified output file
    plt.savefig(output_file)
    plt.close()

def plot_results(pareto_front, save_path=None):

    # Get fitness values for all objectives
    coverage_values = [ind.fitness.values[0] for ind in pareto_front]
    charger_speed_values = [ind.fitness.values[1] for ind in pareto_front]
    num_stations_values = [ind.fitness.values[2] for ind in pareto_front]
    num_chargers_values = [ind.fitness.values[3] for ind in pareto_front]

    # List of titles for each plot
    titles = [
        "Coverage vs Charger Speed",
        "Coverage vs Number of Stations",
        "Coverage vs Number of Chargers",
        "Charger Speed vs Number of Stations",
        "Charger Speed vs Number of Chargers",
        "Number of Stations vs Number of Chargers"
    ]
    
    # List of x and y for each plot
    data_pairs = [
        (coverage_values, charger_speed_values),
        (coverage_values, num_stations_values),
        (coverage_values, num_chargers_values),
        (charger_speed_values, num_stations_values),
        (charger_speed_values, num_chargers_values),
        (num_stations_values, num_chargers_values)
    ]
    
    # Create subplots for each pair of objectives
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.ravel() 

    for i, (x_values, y_values) in enumerate(data_pairs):
        axes[i].scatter(x_values, y_values, color='blue')
        axes[i].set_title(titles[i])
        axes[i].set_xlabel(f"Objective {i+1} Value")
        axes[i].set_ylabel(f"Objective {i+2} Value")
        axes[i].grid(True)

    # Adjust layout
    plt.tight_layout()
    
    # Save the plot if a save_path is provided
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved at {save_path}")
    else:
        plt.show()



def plot_map(data_path, output_path):
    # Load data from the CSV file
    try:
        df = pd.read_csv(data_path)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Check if the necessary columns exist
    required_columns = ['station_id', 'latitude', 'longitude', 'num_chargers', 'charger_speed']
    if not all(col in df.columns for col in required_columns):
        print(f"Missing one or more required columns: {required_columns}")
        return

    # Create Map centered around the average latitude and longitude
    avg_lat = df['latitude'].mean()
    avg_lon = df['longitude'].mean()

    # Create the base map
    station_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

    # Plot all the stations on the map
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Station ID: {row['station_id']}<br>Power: {row['charger_speed']} kW<br>Points: {row['num_chargers']}",
            icon=folium.Icon(color="blue", icon="cloud"),
        ).add_to(station_map)

    # Save the map as an HTML file
    if not output_path.endswith('.html'):
        output_path = os.path.join(output_path, "original_map.html")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the map
    station_map.save(output_path)

    # Output the result
    print(f"Map saved as {output_path}")


