import os
import pandas as pd
import stations
import pre_processing_data
import plotting_EVCS
from nsga import EVCS_Optimization



# Electric vehicle charging stand infrastructure problem
# Using Multi objective Evolutionary Algorithms 
# NSGA-II (Non-dominated Sorting Genetic Algorithm II)

# supposed resutl
# 1. Pareto Front
# 2. Optimal Charging Station Placement
# 3. Cost and Benefit Analysis
# 4. Energy Consumption Efficiency

# visualize the Pareto front.

# Define the objectives
# 1. Coverage: Maximize the geographic area covered by EV charging stations.
# 2: Cost: Minimize the cost of setting up the infrastructure for the charging stations.
# 3. Power Level: Maximize the power level of the stations to improve charging efficiency and reduce waiting times.

# 4. Charging Speed (Efficiency) Maximize the speed of the charging stations, considering faster charging options

# 5: wait time
# daset
# 1. statitons dataset
# https://openchargemap.org
# "key": "65480684-8133-4ba5-9289-949cc656022d"
# run station.py 


# Cost dataset sources:
#   https://theicct.org/wp-content/uploads/2021/06/ICCT_EV_Charging_Cost_20190813.pdf
#1. U.S. Department of Energy (EVSE Report)
#2. Electrify America - Real Charging Stations
#3. Tesla Supercharger Information

# chargers key
#Level 2 Charger is used for lower-power points less, than 50 kW.
#DC Fast Charger is used for stations with power greater than 50 kW.

# Level 1 using a standard 120V outlet, and slower than level 2
# while Level 2 is faster and requires a 240V outlet.

 # Path to your CSV file

# Define the relative path to the file
current_directory = os.getcwd()
url = "https://api.openchargemap.io/v3/poi"
data_path = os.path.join(current_directory, "Datasets", "california_stations.csv")
used_data_path = os.path.join(current_directory, "Datasets", "data.csv")


# Load the datasets
stations_data = pd.read_csv("Datasets/california_stations.csv")
cost_data = pd.read_csv("Datasets/EV_tation_infrastructure_cost.csv")
used_data = pd.read_csv("Datasets/data.csv")

# Set algorithm hyperparameters    
parms = {
    'population_size': 100,
    'generations': 50,
    'mu': 50,
    'lambda_': 100,  
    'cxpb': 0.7,
    'mutpb': 0.2,
    'data_file': used_data_path
}



def main():
    print("Fetch station data...")
    stations.get_stations_data(url, data_path) 

    print("Merege the data")
    pre_processing_data.merege_data(stations_data, cost_data)

    print("Ploatin EVCS befor optimization")
    plotting_EVCS.ploatin_EVCS(used_data)
    
    print("EVCS Optimization")
    optimization = EVCS_Optimization(parms)

    print("Pareto Front")
    pareto_front = optimization.run_algorithm()

    print("Display the results")
    optimization.display_results(pareto_front)

if __name__ == "__main__":
    main()




