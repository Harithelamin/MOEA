print("Start")
# Electric vehicle charging stand infrastructure problem
# Using Multi objective Evolutionary Algorithms 
# NSGA-II (Non-dominated Sorting Genetic Algorithm II)

# supposed resutl
# 1. Pareto Front
# 2. Optimal Charging Station Placement
# 3. Cost and Benefit Analysis
# 4. Energy Consumption Efficiency

# visualize the Pareto front.


# 
# install python libraries

import random
import numpy as np
import pandas as pd
from deap import base, creator, tools
import matplotlib.pyplot as plt
import matplotlib

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

# to avoid error
matplotlib.use('TkAgg')

# Read the dataset
df = pd.read_csv('Datasets/data.csv')

# Remove the dollar sign from 'Cost', then convert to numeric
df['Cost'] = df['Cost'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Split Coordinates into x and y
df[['coverage_x', 'coverage_y']] = df['Coordinates'].str.split(',', expand=True)
df['coverage_x'] = df['coverage_x'].astype(float)
df['coverage_y'] = df['coverage_y'].astype(float)

# Define the objectives problem 
# maximize coverage 
# maximize power to reduce the waiting time
# minimize cost
creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, -1.0))  # Coverage and Power should be maximized, Cost minimized
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Objective Functions
def evaluate(individual):
    """
    Evaluates the individual based on three objectives:
    - Coverage: the area covered by the charging stations.
    - Power Level: the power per charger (either 50W, 150W, 350W).
    - Cost: the total cost based on cost per charger and number of chargers.
    """
    # individual values
    coverage_x = individual[0]
    coverage_y = individual[1]
    power_level_per_charger = individual[2]  # Power level per charger (50W, 150W, or 350W)
    chargers_per_site = individual[3]  # Number of chargers per site
    cost_per_charger = individual[4]  # Cost per charger

    # Coverage: Area covered by the charging station
    coverage = coverage_x * coverage_y

    # Power Level: Total power for the site based on power per charger
    total_power = power_level_per_charger * chargers_per_site  # Total power is power per charger * number of chargers

    # Cost: The total cost of setting up the stations based on cost per charger
    total_cost = cost_per_charger * chargers_per_site  # Total cost = cost per charger * number of chargers

    return coverage, total_power, total_cost

# Generate an individual
def create_individual():
    row = df.sample(1).iloc[0]
    coverage_x = row['coverage_x']
    coverage_y = row['coverage_y']
    
    # Power level per charger should be 50W, 150W, or 350W 
    power_level_per_charger = random.choice([50, 150, 350])
    chargers_per_site = row['Chargers per Site']
    
    # Cost per charger
    cost_per_charger = row['Cost']
    
    return [float(coverage_x), float(coverage_y), power_level_per_charger, int(chargers_per_site), float(cost_per_charger)]

# Set up the toolbox
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxBlend, alpha=0.5)  # Crossover (works with numeric values)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)  # Mutation
toolbox.register("select", tools.selNSGA2)  # NSGA-II Selection
toolbox.register("evaluate", evaluate)

# NSGA-II Algorithm
def main():
    random.seed(42)  # Set seed for reproducibility
    population = toolbox.population(n=100)

    generations = 50
    cx_prob = 0.7  # Crossover probability
    mut_prob = 0.2  # Mutation probability

    for gen in range(generations):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation
        for mutant in offspring:
            if random.random() < mut_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate fitness of individuals with invalid fitness values
        invalid_individuals = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid_individuals))
        for ind, fit in zip(invalid_individuals, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

        # Print the statistics of the current generation
        pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
        pareto_front_fitness = [ind.fitness.values for ind in pareto_front]
        avg_fitness = np.mean(pareto_front_fitness, axis=0)
        print(f"Generation {gen}: Avg Fitness (Coverage, Power, Cost): {avg_fitness}")

    return population

# Visualize the Pareto front
def visualize_pareto_front(population):
    # Pareto front
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    # Extract the fitness values for coverage and power
    coverage = [ind.fitness.values[0] for ind in pareto_front]
    power = [ind.fitness.values[1] for ind in pareto_front]

    # Plot the Pareto front (Coverage vs Power)
    plt.figure(figsize=(10, 6))
    plt.scatter(coverage, power, c='blue', label='Pareto Front')
    plt.xlabel('Coverage (Area)')
    plt.ylabel('Power (W)')
    plt.title('Pareto Front: Coverage vs Power')
    plt.grid(True)
    plt.legend()
    plt.show()

# Visualize the optimal locations of the charging stations
def visualize_optimal_locations(population):
    # Pareto front
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    # Create lists for the station details
    coverage_x_list = []
    coverage_y_list = []
    power_list = []
    chargers_list = []
    total_power_list = []
    total_cost_list = []

    # station details
    for ind in pareto_front:
        coverage_x_list.append(ind[0])
        coverage_y_list.append(ind[1])
        power_list.append(ind[2])  # Power level per charger (50W, 150W, 350W)
        chargers_list.append(ind[3])  # Number of chargers per site
        total_power_list.append(ind[2] * ind[3])  # Total power = Power * Chargers
        total_cost_list.append(ind[4] * ind[3])  # Total cost = cost per charger * number of chargers

    # Plot the optimal locations
    plt.figure(figsize=(12, 8))

    # Plot stations
    plt.scatter(coverage_x_list, coverage_y_list, c='blue', s=100, label="Station Locations")

    # Annotate each station with details
    for i, (x, y, power, chargers, total_power, total_cost) in enumerate(zip(coverage_x_list, coverage_y_list, power_list, chargers_list, total_power_list, total_cost_list)):
        annotation = f"Power: {power}W\nChargers: {chargers}\nTotal Power: {total_power}W\nCost: ${total_cost}"
        plt.text(x + 0.02, y + 0.02, annotation, fontsize=9, ha='left', color='black')

    plt.xlabel("Coverage X Coordinate")
    plt.ylabel("Coverage Y Coordinate")
    plt.title("Optimal Charging Station Locations with Power, Chargers, and Total Power")
    plt.grid(True)

    plt.legend(["Charging Stations"], loc='upper right')

    # Display the plot
    plt.show()

if __name__ == "__main__":
    population = main()
    # Visualize the Pareto front and optimal locations
    visualize_pareto_front(population)
    visualize_optimal_locations(population)
