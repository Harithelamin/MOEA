print("Start")
# install python libraries
import random
from deap import base, creator, tools, algorithms
import numpy as np

# Define the objectives
# 1: cost (Minimize the installation cost of the charging stations)
# 2. Charging Speed (Efficiency) Maximize the speed of the charging stations, considering faster charging options
# 3: User Accessibility Maximize user accessibility, ensuring that charging stations are easy to find and reach for EV users.


# daset
# 1. dataste
# source: Estimating electric vehicle charging infrastructure costs across major U.S. metropolitan areas
# https://theicct.org/wp-content/uploads/2021/06/ICCT_EV_Charging_Cost_20190813.pdf



# Define the problem parameters
Num_stations  = 10   # number of possible charging locations
Min_cost = 5000      # minimum installation cost per station
Max_cost = 20000     # maximum installation cost per station
Max_speed = 3      # Maximum charging speed (50, 150, 350 kw)
Max_accessibility = 10  # Max accessibility per user.

# We will use the NSGA-II algorithm, which works well for multi-objective optimization problems.

# Define the problem as a multi-objective optimization
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0, 1.0))  # Cost: Minimize, Charging Speed: Maximize, Accessibility: Maximize
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Define the evaluation function
def evaluate(individual):
    """
    The evaluation function considers three objectives:
    1. Minimize cost of the stations
    2. Maximize charging speed (efficiency)
    3. Maximize user accessibility
    """

    cost = sum(individual[:Num_stations]) * Max_cost / Num_stations  # cost calculation
    charging_speed = sum(individual[Num_stations:Num_stations*2]) * Max_speed / Num_stations  # charging speed
    accessibility = sum(individual[Num_stations*2:]) * Max_accessibility / Num_stations  # accessibility score

    return cost, charging_speed, accessibility  # Return the three objectives