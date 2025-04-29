import os
import matplotlib.pyplot as plt
import pandas as pd

# Define the objectives problem 
# 1. Maximize coverage
# 2. Maximize charger speed to reduce waiting time
# 3. Minimize stations num
# 4. Minimize chargers num
# 5. Minimize average distance

def plot_trade_off_analysis(pareto_df, save_dir):
    pareto_df['num_stations'] = pareto_df.apply(lambda row: len(str(row['station_id']).split(',')), axis=1)

    # Extract columns
    coverage = pareto_df["coverage"]
    charger_speed = pareto_df["charger_speed"]
    num_stations = pareto_df["num_stations"]
    num_chargers = pareto_df["num_chargers"]    
    avg_distance = pareto_df["average_vehicle_distance_km"]

    # 2D plots for 3*2
    fig, axs = plt.subplots(3, 2, figsize=(14, 15))

    # Plot: Coverage vs Charger Speed
    axs[0, 0].scatter(coverage, charger_speed, c='blue', alpha=0.8)
    axs[0, 0].set_xlabel('Coverage (maximize)')
    axs[0, 0].set_ylabel('Charger Speed (maximize)')
    axs[0, 0].set_title('Coverage vs Charger Speed')

    # Plot: Coverage vs Number of Stations
    axs[0, 1].scatter(coverage, num_stations, c='green', alpha=0.8)
    axs[0, 1].set_xlabel('Coverage (maximize)')
    axs[0, 1].set_ylabel('Number of Stations (minimize)')
    axs[0, 1].set_title('Coverage vs Number of Stations')

    # Plot: Charger Speed vs Number of Stations
    axs[1, 0].scatter(charger_speed, num_stations, c='red', alpha=0.8)
    axs[1, 0].set_xlabel('Charger Speed (maximize)')
    axs[1, 0].set_ylabel('Number of Stations (minimize)')
    axs[1, 0].set_title('Charger Speed vs Number of Stations')

    # Plot: Number of Stations vs Number of Chargers
    axs[1, 1].scatter(num_stations, num_chargers, c='purple', alpha=0.8)
    axs[1, 1].set_xlabel('Number of Stations (minimize)')
    axs[1, 1].set_ylabel('Number of Chargers (minimize)')
    axs[1, 1].set_title('Number of Stations vs Number of Chargers')

     # Plot: Avg Distance vs Number of Stations
    axs[2, 1].scatter(avg_distance, num_stations, c='teal', alpha=0.8)
    axs[2, 1].set_xlabel('Avg Vehicle Distance (minimize)')
    axs[2, 1].set_ylabel('Number of Stations (minimize)')
    axs[2, 1].set_title('Avg Distance vs Number of Stations')


    plt.tight_layout()

    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)

    # Save plot
    plot_path = os.path.join(save_dir, "Trade_Off.png")
    plt.savefig(plot_path)
    plt.close()


def main():
    current_directory = os.getcwd()
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data_with_covarage.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Load the optimized data (Pareto front)
    pareto_front = pd.read_csv(optimized_data_path)

    # Plot and save the Trade-off analysis
    plot_trade_off_analysis(pareto_front, save_dir)


if __name__ == "__main__":
    main()
