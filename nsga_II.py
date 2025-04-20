# Reference
# DEAP Documentation: https://deap.readthedocs.io/en/master/
# NSGA-II (NSGA2) in DEAP: https://deap.readthedocs.io/en/master/tutorials/faq.html#how-can-i-use-nsga2
# Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002). "A fast and elitist multiobjective genetic algorithm: NSGA-II". IEEE Transactions on Evolutionary Computation, 6(2), 182–197.
# Geopy Documentation: https://geopy.readthedocs.io/en/stable/
# Pandas Documentation: https://pandas.pydata.org/pandas-docs/stable/
# Matplotlib Documentation: https://matplotlib.org/stable/contents.html
# Coello, C. A. C. (2006). Evolutionary Multi-objective Optimization: A Historical View of the Field. In: Handbook of Evolutionary Computation. Oxford University Press.
# Nagar, S. (2019). Hands-On Genetic Algorithms with Python: Solving Optimization Problems with Python. Packt Publishing.



import os
import pandas as pd
import random
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from geopy.distance import geodesic
import numpy as np

# NSGA-II Algorithm
# to optimize multiple objectives: 
# 1. Maximize coverage
# 2. Maximize charger speed to reduce waiting time
# 3. Minimize stations number to minimizing cost
# 4. Minimize chargers number to minimizing cost
# 5. minimizing cost. No action. 
# The goal is to develop a solution that finds a balance between these objectives.


# Define the objectives problem 
# 1. Maximize coverage
# 2. Maximize charger speed to reduce waiting time
# 3. Minimize stations num
# 4. Minimize chargers num



class EVCS_Optimization:
    def __init__(self, parms):
        # Initializing the data and other parameters
        self.data = pd.read_csv(parms['data_file'])
        self.optimized_data_file = parms['optimized_data_file']
        self.num_generations = parms['generations']
        self.population_size = parms['population_size']
        self.cx_prob = parms['cxpb']
        self.mut_prob = parms['mutpb']
        self.mu = parms['mu']
        self.lambda_ = parms['lambda_']
        self.power_levels = [11.5, 14.2, 19.2, 25, 60, 62, 80, 120, 150, 180, 200, 240, 250, 300, 325, 350, 400]
        self.toolbox = None
        self.population = None

        # Create problem using DEAP
        # Maximize coverage
        # Maximize charger speed 
        # Minimize stations num
        # Minimize chargers num
        creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, -1.0, -1.0))  
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        # Initialize toolbox
        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", self.cxTwoPointCheck)
        self.toolbox.register("mutate", self.mutShuffleIndexesCheck, indpb=0.2)
        self.toolbox.register("select", tools.selNSGA2)
        self.toolbox.register("evaluate", self.evaluate)

        # Initialize population
        self.population = self.toolbox.population(n=self.population_size)

    # Define objectives
    # Objective 1: Maximize Coverage
    def calculate_coverage(self, stations):
        coverage = 0
        for i in range(len(stations)):
            for j in range(i + 1, len(stations)):
                station1 = self.data.iloc[stations[i]]
                station2 = self.data.iloc[stations[j]]
                distance = geodesic((station1['latitude'], station1['longitude']),
                                    (station2['latitude'], station2['longitude'])).km
                coverage += distance
        return coverage

    # Objective 2: Maximize Charger Speed
    def calculate_charger_speed(self, stations):
        return max(self.data.iloc[station]['charger_speed'] for station in stations) if stations else 0

    # Objective 3: Minimize the Number of Stations
    def calculate_num_stations(self, stations):
        return len(stations)

    # Objective 4: Minimize the Number of Chargers
    def calculate_num_chargers(self, stations):
        return sum(self.data.iloc[station]['num_chargers'] for station in stations)

    # Define the evaluation function that combines all objectives
    def evaluate(self, individual):
        coverage = self.calculate_coverage(individual)
        charger_speed = self.calculate_charger_speed(individual)
        num_stations = self.calculate_num_stations(individual)
        num_chargers = self.calculate_num_chargers(individual)
        return coverage, charger_speed, num_stations, num_chargers

    # Create a random individual with fewer stations selected
    def create_individual(self):
        num_stations = random.randint(1, len(self.data) // 2)
        return random.sample(range(len(self.data)), num_stations)
    
    # Crossover combines the features of two parents individuals
    # To create one or more "children"

    # Crossover function with added size check to minimize station numbers

    # cxTwoPoint is a two-point crossover function
    # It selects two random points in the parents
    # Then swaps the segments between those points to produce two new children.
    def cxTwoPointCheck(self, ind1, ind2):
        if len(ind1) < 2 or len(ind2) < 2:
            return ind1, ind2
        return tools.cxTwoPoint(ind1, ind2)

    # Mutation makes small random changes to individuals.
    # It helps maintain genetic diversity
    # Mutation function to reduce the number of stations.

    # we need mutShuffleIndexes to Keeps the solution valid (no duplicates or missing values)
    def mutShuffleIndexesCheck(self, individual, indpb):
        if len(individual) > 1:
            if random.random() < indpb:
                individual.remove(random.choice(individual))
        return individual, 

    # Run the algorithm
    def run(self):
        # Initialize stats, halloffame

        # We need stats to monitoring the performance of the algorithm over time.
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        # Use Hall of Fame (HoF)
        # To record of the best individuals found over the entire run of an evolutionary algorithm
        
        # To Keep the best individual
        halloffame = tools.HallOfFame(1)  

        # Run NSGA-II algorithm 
        algorithms.eaMuPlusLambda(self.population, self.toolbox, mu=self.mu, lambda_=self.lambda_, 
                                  cxpb=self.cx_prob, mutpb=self.mut_prob, ngen=self.num_generations,
                                  stats=stats, halloffame=halloffame, verbose=True)

        # Extract the Pareto front (non-dominated solutions)
        pareto_front = tools.sortNondominated(self.population, len(self.population), first_front_only=True)[0]

        # Collect and save optimized data
        self.save_optimized_data(pareto_front)

        # Plot results
        self.plot_results(pareto_front)

    def save_optimized_data(self, pareto_front):
        optimized_data = []

        for ind in pareto_front:
            selected_stations = {}

            for station in ind:
                station_data = self.data.iloc[station]
                station_id = station_data['station_id']
                latitude = station_data['latitude']
                longitude = station_data['longitude']
                charger_speed = station_data['charger_speed']

                if station_id not in selected_stations:
                    selected_stations[station_id] = {
                        'latitude': latitude,
                        'longitude': longitude,
                        'charger_speed': charger_speed,
                        'num_points': 1
                    }
                else:
                    selected_stations[station_id]['num_points'] += 1

            for station_id, data in selected_stations.items():
                optimized_data.append([station_id,
                                       data['latitude'],
                                       data['longitude'],
                                       data['num_points'],
                                       data['charger_speed']])

        # Create DataFrame as original data, and save to CSV
        optimized_df = pd.DataFrame(optimized_data, columns=["station_id", "latitude", "longitude", "number_of_points", "charger_speed"])
        optimized_df = optimized_df.drop_duplicates(subset='station_id', keep='first')
        optimized_df.to_csv(self.optimized_data_file, index=False)

        print(f"Optimized data saved to {self.optimized_data_file}")

    def plot_results(self, pareto_front):
        coverage_values = [ind.fitness.values[0] for ind in pareto_front]
        charger_speed_values = [ind.fitness.values[1] for ind in pareto_front]

        plt.figure(figsize=(6, 4))
        plt.scatter(coverage_values, charger_speed_values, color='blue')
        plt.title('Objective 1: Coverage vs Objective 2: Charger Speed')
        plt.xlabel('Coverage (km)')
        plt.ylabel('Charger Speed (kW)')
        plt.grid(True)
        plt.show()

def main():
    # Get the current directory
    current_directory = os.getcwd()

    # Define the path files
    data_path = os.path.join(current_directory, "Datasets", "stations.csv")
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

    # Create the EVCS_Optimization object
    optimization = EVCS_Optimization(parms)

    # Run the optimization
    optimization.run()

if __name__ == "__main__":
    main()
