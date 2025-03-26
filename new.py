import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data(optimized_data_path):
    """
    Load the optimized data from the CSV file.

    Parameters:
    optimized_data_path (str): Path to the optimized data CSV file.

    Returns:
    pd.DataFrame: DataFrame containing the optimized data.
    """
    return pd.read_csv(optimized_data_path)

def plot_convergence(pareto_front, output_file):
    """
    Plot the convergence of the Pareto front based on latitude and longitude.

    Parameters:
    pareto_front (pd.DataFrame): DataFrame containing the Pareto front data with 'latitude' and 'longitude' columns.
    output_file (str): Path to save the convergence plot.
    """
    plt.scatter(pareto_front['latitude'], pareto_front['longitude'], color='blue')

    # Set labels and title for the plot
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Convergence Plot')

    # Save the plot to the specified output file
    plt.savefig(output_file)
    plt.close()

def main():
    current_directory = os.getcwd()  # Get the current working directory
    optimized_data_path = os.path.join(current_directory, "Datasets", "stations.csv")

    # Load the data from the CSV file
    pareto_front = load_data(optimized_data_path)

    # Check if the necessary columns exist
    if 'latitude' not in pareto_front.columns or 'longitude' not in pareto_front.columns:
        print("Error: The 'latitude' and 'longitude' columns are required in the data.")
        return

    # Create the output directory for the plots if it doesn't exist
    output_directory = os.path.join(current_directory, 'Figures')
    os.makedirs(output_directory, exist_ok=True)

    # Define the path to save the convergence plot
    convergence_plot_path = os.path.join(output_directory, 'convergence_plot.png')

    # Generate and save the convergence plot
    plot_convergence(pareto_front, convergence_plot_path)

    print(f"Convergence plot saved at: {convergence_plot_path}")

if __name__ == "__main__":
    main()
