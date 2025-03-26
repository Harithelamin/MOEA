# Reference
# For Genetic, and NSGA-II algorithm.
# DEAP Documentation: https://deap.readthedocs.io/en/master/
# NSGA-II (NSGA2) in DEAP: https://deap.readthedocs.io/en/master/tutorials/faq.html#how-can-i-use-nsga2
# Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002). "A fast and elitist multiobjective genetic algorithm: NSGA-II". IEEE Transactions on Evolutionary Computation, 6(2), 182–197.
# Geopy Documentation: https://geopy.readthedocs.io/en/stable/
# Pandas Documentation: https://pandas.pydata.org/pandas-docs/stable/
# Matplotlib Documentation: https://matplotlib.org/stable/contents.html
# Coello, C. A. C. (2006). Evolutionary Multi-objective Optimization: A Historical View of the Field. In: Handbook of Evolutionary Computation. Oxford University Press.
# Nagar, S. (2019). Hands-On Genetic Algorithms with Python: Solving Optimization Problems with Python. Packt Publishing.

# For openchargemap, and requests from api.
# https://requests.readthedocs.io/en/latest/api/#requests.get
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
# https://openchargemap.org/site/develop/api

# For visualization.
# Official documentation for Matplotlib, which is used for creating plots.
# Link: https://matplotlib.org/stable/contents.html
import os
import pandas as pd
from nsga_II import EVCS_Optimization
import plot
print(dir(plot))
import stations 
import cost



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


def main():
    # stations url path
    url = "https://api.openchargemap.io/v3/poi"
    # Path to the dataset
    current_directory = os.getcwd()
    data_path = os.path.join(current_directory, "Datasets", "stations.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data.csv")
    original_map_path = os.path.join(current_directory, "Figures")
    optimized_map_path = os.path.join(current_directory, "Figures")
    output_directory = os.path.join(current_directory, "Figures")



    # Set hyperparameters    
    parms = {
        'population_size': 100,
        'generations': 50,
        'mu': 50,
        'lambda_': 100,
        'cxpb': 0.7,
        'mutpb': 0.2,
        'data_file': data_path,
        'optimized_data_file': optimized_data_path
    }

    print("Fetching station data...")
    #stations.get_stations_data(url, data_path)  

    print("Calcuate the cost for original data...")
    #cost.calculatin_process(data_path)

    
    print("Calcuate the cost for obtimized data...")
    #cost.calculatin_process(data_path)

    # Create the EVCS_Optimization object
    #optimization = EVCS_Optimization(parms)

    # Run the optimization
    #optimization.run()

    # plot to visualize the results

    print("Plot the results...")

    #plot.plot_results(optimization.population, optimized_map_path) 
    # 
    #plot.plot_map(data_path, original_map_path) 
    #plot.plot_map(optimized_data_path, optimized_map_path) 


    # Load the optimized data (Pareto front)
    def load_optimized_data(file_path):
        return pd.read_csv(file_path)

    # Load optimized data (Pareto front)
    pareto_front = load_optimized_data(optimized_data_path)

    #print(pareto_front)
    # Define the path to save the convergence plot
    convergence_plot_path = os.path.join(output_directory, 'convergence_plot.png')
    objective_distribution_path =os.path.join(current_directory, "objective_distribution.png")

    # Generate and save the convergence plot
    #plot_convergence(pareto_front, convergence_plot_path)

    #plot_objective_distribution(pareto_front, objective_distribution_path)

    #print(pareto_front.columns)


    #plot.plot_objective(pareto_front, output_directory)
    #print(pareto_front)





if __name__ == "__main__":
    main()