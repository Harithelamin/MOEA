# Reference
# Official documentation for Matplotlib, which is used for creating plots.
# Link: https://matplotlib.org/stable/contents.html
import matplotlib.pyplot as plt

def plot_results(pareto_front, save_path=None):
    """
    Plots all objectives against each other in a matrix format:
    - Coverage vs Charger Speed
    - Coverage vs Number of Stations
    - Coverage vs Number of Chargers
    - Charger Speed vs Number of Stations
    - Charger Speed vs Number of Chargers
    - Number of Stations vs Number of Chargers
    
    :param pareto_front: List of individuals in the pareto front
    :param save_path: Path to save the plot. If None, the plot is shown, but not saved.
    """

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



import pandas as pd
import folium
import os

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


