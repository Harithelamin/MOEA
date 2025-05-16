# The code reference
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
from matplotlib.pyplot import plot
import pandas as pd
import add_coverage_to_optimized_data
import add_distance_to_optimized_data
from nsga_II import EVCS_Optimization
import nsga_II
import stations 
import calculate_evcs_cost
import update_vehicles_with_coord
import add_coverage_to_station_data
import add_distance_to_stations_data



# Electric vehicle charging stand infrastructure problem
# Using Multi objective Evolutionary Algorithms 
# NSGA-II (Non-dominated Sorting Genetic Algorithm II)

# supposed resutl
# 1. Pareto Front
# 2. Optimal Charging Station Placement
# 3. Cost and Benefit Analysis
# 4. Energy Consumption Efficiency



# Define the objectives problem 
# 1. Maximize coverage
# 2. Maximize charger speed to reduce waiting time
# 3. Minimize stations num
# 4. Minimize chargers num
# 5. Min avg_distance




# visualize the Pareto front.

# Define the objectives problem 
# 1. Maximize coverage
# 2. Maximize charger speed to reduce waiting time
# 3. Minimize stations num
# 4. Minimize chargers num
# 5. Min avg_distance



# 2. Cost dataset sources:
#   https://theicct.org/wp-content/uploads/2021/06/ICCT_EV_Charging_Cost_20190813.pdf

# 3. EVs dataset from California city
# https://data.ca.gov/dataset/vehicle-fuel-type-count-by-zip-code


#1. U.S. Department of Energy (EVSE Report)
#2. Electrify America - Real Charging Stations
#3. Tesla Supercharger Information

# chargers key
#Level 2 Charger is used for lower-power points less, than 50 kW.
#DC Fast Charger is used for stations with power greater than 50 kW.

# Level 1 using a standard 120V outlet, and slower than level 2
# while Level 2 is faster and requires a 240V outlet.


def main():
    print("Fetching station data, and preprocessing it...")
    stations.main 

    print("Fetching EV data, and preprocessing it...")
    update_vehicles_with_coord.main 

    print("Add coverage to original station data...")
    add_coverage_to_station_data.main

    print("Add distance to original station data...")
    add_distance_to_stations_data.main

    print("Run NSGA-II to Optimization EVCS...")
    nsga_II.main

    print("Add coverage to optimized data...")
    add_coverage_to_optimized_data.main

    print("Add distance to optimized  data...")
    add_distance_to_optimized_data.main
    
    print("Calculate Originla EVCS Network...")
    print("Calculate Optimized EVCS Network...")
    calculate_evcs_cost.main

    


if __name__ == "__main__":
    main()