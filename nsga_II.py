import os
import pandas as pd
import random
from deap import base, creator, tools
import matplotlib.pyplot as plt
import numpy as np

# NSGA-II Algorithm
# to optimize multiple objectives: 
# 1. maximizing coverage, 
# 2. maximizing power (to reduce waiting time), 
# 3. minimizing cost. 
# The goal is to develop a solution that finds a balance between these objectives.


# Define the objectives problem 
# maximize coverage 
# maximize power to reduce the waiting time
# minimize cost


class StationOptimization:
    def __init__(self, parms):
        # Initializing the data and other parameters
        self.data = pd.read_csv(parms['data_file']) 
        self.optimized_data_path = parms['optimized_data_file'] 
        self.num_generations = parms['generations']  
        self.population_size = parms['population_size']
        self.cx_prob = parms['cxpb']
        self.mut_prob = parms['mutpb']
        self.num_stations = parms['mu'] 
        self.power_levels = [14.2, 11.5, 19.2, 25, 60, 62, 80, 120, 150, 180, 200, 240, 250, 300, 325, 350, 400]
        self.toolbox = None
        self.population = None

        # Create problem using DEAP
        # Maximize coverage, 
        # minimize points, 
        # maximize power_kw
        creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, 1.0)) 
        creator.create("Individual", list, fitness=creator.FitnessMulti)

    # Define objectives
    def evaluate(self, individual):
        # Set Individual as a list of station
        selected_stations = self.data.iloc[individual]
        
        # Define California's latitude and longitude bounds
        valid_lat_range = (32.5343, 42.0095)  
        valid_lon_range = (-124.4096, -114.1312) 
        
        # Filter out stations that are outside of California's bounds
        valid_stations = selected_stations[ 
            (selected_stations['latitude'] >= valid_lat_range[0]) & 
            (selected_stations['latitude'] <= valid_lat_range[1]) & 
            (selected_stations['longitude'] >= valid_lon_range[0]) & 
            (selected_stations['longitude'] <= valid_lon_range[1])
        ]
        
        # If no valid stations are selected, return a very low coverage
        if len(valid_stations) == 0:
            return (0, float('inf'), 0)  # invalid location
        
        # OBJECTIVE 1: Maximizing Coverage
        # Coverage: number of unique locations covered the area
        unique_locations = valid_stations[['latitude', 'longitude']].drop_duplicates()
        coverage = len(unique_locations)  # Number of unique locations

        # OBJECTIVE 2: Minimizing Cost
        # Total number of points 
        points = valid_stations['number_of_points'].sum()

        # OBJECTIVE 3: Maximizing Power
        # Power_kw: randomly select a power kw for each selected station 
        power_kw = sum(random.choice(self.power_levels) for _ in range(len(valid_stations)))
        
        return (coverage, points, power_kw)

    def setup_toolbox(self):
        self.toolbox = base.Toolbox()
        
        # Create individuals randomly from the data
        self.toolbox.register("attr_int", random.randint, 0, len(self.data) - 1)
        # Select 10 stations for an individual
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_int, n=self.num_stations)  
        # Corrected population initialization
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)  

        # Register evaluation function
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
        self.toolbox.register("select", tools.selNSGA2)
        self.toolbox.register("evaluate", self.evaluate)

    def run_algorithm(self):
        # Create a population using population size
        self.population = self.toolbox.population(n=self.population_size)  

        # Run the algorithm
        for gen in range(self.num_generations):
            print(f"Generation {gen}")
            
            # Select the next generation of individuals
            offspring = self.toolbox.select(self.population, len(self.population))
            
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))
            
            # Apply crossover and mutation to create the next generation
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.cx_prob:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            
            for mutant in offspring:
                if random.random() < self.mut_prob:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
            
            # Evaluate individuals with invalid fitness
            invalid_individuals = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_individuals)
            for ind, fit in zip(invalid_individuals, fitnesses):
                ind.fitness.values = fit
            
            # Replace the old population with the new one
            self.population[:] = offspring
            
            # Print statistics of the current generation
            front = tools.sortNondominated(self.population, len(self.population), first_front_only=True)[0]
            front_fitness = [ind.fitness.values for ind in front]
            print(f"Best Fitness: {front_fitness[0]}")

    def collect_optimized_data(self):
        # Get the Pareto-optimal solutions (first front)
        front = tools.sortNondominated(self.population, len(self.population), first_front_only=True)[0]

        # Collect the final Pareto-optimal individuals
        optimized_data = []
        for ind in front:
            selected_stations = self.data.iloc[ind]  # Get selected stations for each individual
            row = selected_stations[['latitude', 'longitude', 'number_of_points', 'power_kw']].copy()  # Copy the relevant data
            row['coverage'] = ind.fitness.values[0]  # Coverage (from fitness)
            row['number_of_points'] = row['number_of_points'].sum()  # Sum of number_of_points for the selected stations
            row['power_kw'] = [random.choice(self.power_levels) for _ in range(len(selected_stations))]  # Randomly choose power_kw
            optimized_data.append(row)

        # Convert to DataFrame and remove duplicates for unique stations only
        optimized_data = pd.concat(optimized_data, ignore_index=True)
        optimized_data = optimized_data.drop_duplicates(subset=['latitude', 'longitude'], keep='first')

        # Save to CSV
        optimized_data.to_csv(self.optimized_data_path, index=False)

        print("Optimized data saved")
        return optimized_data       
    


def main():
    # Path to the dataset
    current_directory = os.getcwd()
    data_path = os.path.join(current_directory, "Datasets", "station_cost.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data.csv")

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

    # Initialize the optimization class
    optimizer = StationOptimization(parms)  

    # Setup toolbox for DEAP
    optimizer.setup_toolbox()

    # Run the algorithm
    optimizer.run_algorithm()

    # Collect optimized data and save to CSV
    optimized_data = optimizer.collect_optimized_data()

    # Plot results
    optimizer.plot_results(optimized_data)

if __name__ == "__main__":
    main()
