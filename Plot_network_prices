import os

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def plot_EVCS_cost(save_dir, original_data_path, optimized_data_path, column='station_cost'):
    # Original data
    original_data = pd.read_csv(original_data_path)
    Original_EVCS_cost = original_data[column].sum()


    # Optimized data
    Optimized_data = pd.read_csv(optimized_data_path)
    Optimized_EVCS_cost = Optimized_data[column].sum()

    # Bar chart data
    labels = ['Original EVCS Cost', 'Optimized EVCS Cost']
    values = [Original_EVCS_cost, Optimized_EVCS_cost]
    colors = ['red', 'blue']

        # Plot bar chart
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, values, color=colors)

    # Add value labels on top
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.01 * yval, f'{yval:,.0f}', ha='center', va='bottom')
        

    plt.title("EVCS Total Cost Comparison")
    plt.ylabel("Total Cost")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "plot_EVCS_cost.png")
    plt.savefig(save_path)
    print(f"Plot saved to: {save_path}")



def main():
    current_directory = os.getcwd()
    original_data_path = os.path.join(current_directory, "Datasets", "station_cost_before_obtimized.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "station_cost_after_obtimized.csv")
    save_dir = os.path.join(current_directory, "Fig")

    # Plot station_cost
    plot_EVCS_cost(save_dir, original_data_path, optimized_data_path, column='station_cost')

if __name__ == "__main__":
    main()