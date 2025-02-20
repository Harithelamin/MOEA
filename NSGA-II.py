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





# Read the dataset
df = pd.read_csv('Datasets/data.csv')

# Remove the dollar sign and commas from 'Cost', then convert to numeric
df['Cost'] = df['Cost'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Split Coordinates into x and y
df[['coverage_x', 'coverage_y']] = df['Coordinates'].str.split(',', expand=True)
df['coverage_x'] = df['coverage_x'].astype(float)
df['coverage_y'] = df['coverage_y'].astype(float)

# Define the problem objectives (maximize coverage and power, minimize cost)
creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, -1.0))  # Coverage and Power should be maximized, Cost minimized
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Objective Functions
def evaluate(individual):
    """
    Evaluates the individual based on three objectives:
    - Coverage: the area covered by the charging stations.
    - Power Level: the power per site (either 150 or 350) to reduce charging time.
    - Cost: the cost of setting up the charging infrastructure.
    """
    # Extract individual values
    coverage_x = individual[0]
    coverage_y = individual[1]
    power_level_per_site = individual[2]  # 50, 150 or 350
    chargers_per_site = individual[3]  # Number of chargers per site
    cost_per_site = individual[4]  # Cost per site

    # Coverage
    coverage = coverage_x * coverage_y

    # Power Level: Total power per site for reducing charging time
    total_power = power_level_per_site * chargers_per_site  # Total power per site

    # Cost: The total cost of setting up the stations
    total_cost = cost_per_site  # Total setup cost for the site

    return coverage, total_power, total_cost

# Generate an individual
def create_individual():
    # Randomly pick a row from the dataset
    row = df.sample(1).iloc[0]
    
    # Create individual from the data (coverage_x, coverage_y, power_level_per_site, chargers_per_site, cost_per_site)
    coverage_x = row['coverage_x']
    coverage_y = row['coverage_y']
    
    # Power level should be 50, 150 or 350 (maximize power level to reduce charging time)
    power_level_per_site = random.choice([50, 150, 350])
    chargers_per_site = row['Chargers per Site']
    cost_per_site = row['Cost']
    
    # Ensure all values are numeric (floats or ints)
    return [float(coverage_x), float(coverage_y), power_level_per_site, int(chargers_per_site), float(cost_per_site)]

# Set up the toolbox
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxBlend, alpha=0.5)  # Crossover (works with numeric values)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)  # Mutation
toolbox.register("select", tools.selNSGA2)  # NSGA-II Selection
toolbox.register("evaluate", evaluate)

# NSGA-ll Algorithm
def main():
    # Set seed for reproducibility
    random.seed(42)  

    # Create the population
    population = toolbox.population(n=100)

    # Algorithm parameters
    generations = 50
    cx_prob = 0.7  # Crossover probability
    mut_prob = 0.2  # Mutation probability

    # Evolutionary Algorithm loop
    for gen in range(generations):
        # Select the next generation of individuals
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

def visualize_optimal_locations(population):
    # Extract the optimal locations from the Pareto front
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

   

if __name__ == "__main__":
    population = main()
    # Visualize the optimal charging station locations from the Pareto front
    visualize_optimal_locations(population)
