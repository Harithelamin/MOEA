import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_nsga_II(data_path, save_dir):
    nsga_log = pd.read_csv(data_path)

    # Plot the relevant columns 
    plt.figure(figsize=(10, 6))
    plt.plot(nsga_log['gen'], nsga_log['avg'], label="Average", color='b', marker='o')
    plt.plot(nsga_log['gen'], nsga_log['std'], label="Standard Deviation", color='r', marker='x')
    plt.plot(nsga_log['gen'], nsga_log['min'], label="Min", color='g', marker='^')
    plt.plot(nsga_log['gen'], nsga_log['max'], label="Max", color='m', marker='s')

    plt.xlabel('Generation')
    plt.ylabel('Objective Value')
    plt.title('NSGA-II Metrics Over Generations')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plot
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "nsga2_metrics.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

    plt.close()

def main():
    current_directory = os.getcwd()
    data_path = os.path.join(current_directory, "nsga2_log.csv")
    save_dir = os.path.join(current_directory, "Fig")

    plot_nsga_II(data_path, save_dir)

if __name__ == "__main__":
    main()
