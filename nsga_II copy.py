# Reference
# DEAP Documentation: https://deap.readthedocs.io/en/master/
# NSGA-II (NSGA2) in DEAP: https://deap.readthedocs.io/en/master/tutorials/faq.html#how-can-i-use-nsga2
# Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002). "A fast and elitist multiobjective genetic algorithm: NSGA-II". IEEE Transactions on Evolutionary Computation, 6(2), 182–197.
# Geopy Documentation: https://geopy.readthedocs.io/en/stable/
# Pandas Documentation: https://pandas.pydata.org/pandas-docs/stable/
# Matplotlib Documentation: https://matplotlib.org/stable/contents.html
# Coello, C. A. C. (2006). Evolutionary Multi-objective Optimization: A Historical View of the Field. In: Handbook of Evolutionary Computation. Oxford University Press.
# Nagar, S. (2019). Hands-On Genetic Algorithms with Python: Solving Optimization Problems with Python. Packt Publishing.


# Vehicel dataset from California city
# https://data.ca.gov/dataset/vehicle-fuel-type-count-by-zip-code

import math
import os
import pandas as pd
import random
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from geopy.distance import geodesic
import numpy as np
from scipy.spatial import cKDTree as KDTree


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
# 5. Min avg_distance


# 7 Station Accessibility. A lower average distance means EVs are generally close to the station
# Minimize avg_distance



class EVCS_Optimization:
    def __init__(self, parms):
        # Initializing the data and other parameters
        self.evcs_data = pd.read_csv(parms['evcs_data'])
        self.EV_data = pd.read_csv(parms['EV_data'])
        self.num_stations = len(self.evcs_data)
        self.optimized_data_file = parms['optimized_data_file']
        self.num_generations = parms['generations']
        self.population_size = parms['population_size']
        self.cx_prob = parms['cxpb']
        self.mut_prob = parms['mutpb']
        self.mu = parms['mu']
        self.lambda_ = parms['lambda_']
        # Available chargers speed
        #self.charger_speed = [11.5, 14.2, 19.2, 25, 60, 62, 80, 120, 150, 180, 200, 240, 250, 300, 325, 350, 400]
        
        self.charger_speed = [50, 60, 62, 80, 120, 150, 180, 200, 240, 250, 300, 325, 350, 400]


        # Define the KDTree for distance lookups in EV dataset
        self.ev_coords = self.EV_data[['latitude', 'longitude']].values
        self.ev_tree = KDTree(self.ev_coords)


        # Define toolbox
        self.toolbox = base.Toolbox()
        self._setup()    

    # Deep setup
    def _setup(self):
        """Sets up the DEAP optimization framework."""
        # Create problem using DEAP
        # Maximize coverage
        # Maximize charger speed 
        # Minimize stations num
        # Minimize chargers num
        # Minimize average dsitance
        creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, -1.0, -1.0, -1.0))
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        self.toolbox.register("attr_bool", random.randint, 0, 1)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, n=self.num_stations)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selNSGA2)
        self.toolbox.register("evaluate", self.evaluate)

    # Calculate weighted by ev demand
    def calculate_weighted_by_ev_demand(self, station_row):
        # Calculates EV demand based on coverage radius and local EVs using KDTree
        coverage_radius = 5  # km
        # Use KDTree to find all EVs within the coverage radius
        station_coord = (station_row['latitude'], station_row['longitude'])
        indices = self.ev_tree.query_ball_point(station_coord, coverage_radius)
        return len(indices)
    # Objective 1 :Maximize coverage of EVs within the coverage radius (5 km).
    def calculate_coverage(self, selected_stations):
        coverage_radius = 5  # km
        covered = set()
        for _, s_row in selected_stations.iterrows():
            station_coord = (s_row['latitude'], s_row['longitude'])
            indices = self.ev_tree.query_ball_point(station_coord, coverage_radius)
            covered.update(indices)
        return len(covered)

    # Objective 2: Maximize charger speed weighted by local EV demand
    def calculate_charger_speed(self, selected_stations):
        # set 50 kw as minimum value to insure levele 3
        minimum_charger_speed = 50  # Minimum speed
        total_weighted_power = 0
        total_demand = 0

        for _, row in selected_stations.iterrows():
            demand = self.calculate_weighted_by_ev_demand(row)
            speed = row['charger_speed']
            num_chargers = row['num_chargers']

            # Penalize if speed is below 50 kW
            if speed < minimum_charger_speed:
                # Count 10% of the real speed
                # Reduce contribution for slow chargers
                penalty_factor = 0.1  
                # If the charger speed is less than 50 kW,
                # reduce its impact by 90%.
                # This solution, will not affected other objectives.
                effective_speed = speed * penalty_factor if speed < 50 else speed
                #effective_speed = speed * penalty_factor
            else:
                effective_speed = speed

            power = effective_speed * num_chargers
            total_weighted_power += power * demand
            total_demand += demand

        # in case devision by 0    
        if total_demand <= 0 or math.isnan(total_demand) or math.isinf(total_demand):
            return 0.0    

        return total_weighted_power / total_demand

    # Objective 3: Minimize the number of stations, weighted by EV demand
    def calculate_num_stations(self, selected_indices):
        return len(selected_indices)

    # Objective 4: Minimize the number of chargers weighted by EV demand
    def calculate_num_chargers(self, selected_stations):
        return selected_stations['num_chargers'].sum()

    # Objective 5: Minimize the average distance to the closest station
    def calculate_avg_ev_distance(self, selected_stations):
        distances = []
        for _, ev_row in self.EV_data.iterrows():
            min_dist = min([geodesic((ev_row['latitude'], ev_row['longitude']),
                                    (s_row['latitude'], s_row['longitude'])).km for _, s_row in selected_stations.iterrows()])
            distances.append(min_dist)
        return np.mean(distances) if distances else float('inf')
    # Evaluates the objectives for a given individual stations
    def evaluate(self, individual):
        selected_indices = [i for i, bit in enumerate(individual) if bit == 1]

        print(f"Evaluating individual: {selected_indices}")

        if not selected_indices:
            return 0, 0, self.num_stations, 0, float('inf')

        selected_stations = self.evcs_data.iloc[selected_indices]

        coverage_score = self.calculate_coverage(selected_stations)
        charger_speed = self.calculate_charger_speed(selected_stations)
        num_stations = self.calculate_num_stations(selected_indices)
        num_chargers = self.calculate_num_chargers(selected_stations)
        avg_distance = self.calculate_avg_ev_distance(selected_stations)

        return coverage_score, charger_speed, num_stations, num_chargers, avg_distance

    # Saves the optimized data to CSV
    def save_optimized_data(self, pareto_front):
        best_solution = pareto_front[0]  
        selected_indices = [i for i, bit in enumerate(best_solution) if bit == 1]
        optimized_stations = self.evcs_data.iloc[selected_indices]
        optimized_stations.to_csv(self.optimized_data_file, index=False)



    def run(self):
        """Runs the NSGA-II optimization algorithm."""
        population = self.toolbox.population(n=self.population_size)
        logbook = tools.Logbook()

         # Initialize logbook
        logbook = tools.Logbook()
        logbook.header = ["gen", "nevals", "avg", "std", "min", "max"]

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

        # Run the algorithm
        population, logbook = algorithms.eaMuPlusLambda(
            population, self.toolbox,
            mu=self.mu, lambda_=self.lambda_,
            cxpb=self.cx_prob, mutpb=self.mut_prob,
            ngen=self.num_generations,
            stats=stats,
            halloffame=halloffame,
            verbose=True
        )

        # Save the algorithm log in csv file
        # Convert logbook to DataFrame
        log_df = pd.DataFrame(logbook)

        # Rround numeric columns for cleaner output
        log_df = log_df.round(10)

        # Save the log to CSV
        log_df.to_csv("nsga2_log.csv", index=False)
        print("nsga2_log saved to nsga2_log.csv")

        # Extract final Pareto front
        pareto_front = tools.sortNondominated(population, k=len(population), first_front_only=True)[0]
        results = [ind.fitness.values for ind in pareto_front]

        # Collect and save optimized data
        self.save_optimized_data(pareto_front)

        return population, pareto_front, results
    
# Main function 
def main():
    # Get the current directory
    current_directory = os.getcwd()

    # Define the path files
    evcs_data = os.path.join(current_directory, "Datasets", "stations.csv")
    EV_data = os.path.join(current_directory, "Datasets", "vehice_data_with_coordinates.csv")
    optimized_data_path = os.path.join(current_directory, "Datasets", "optimized_data.csv")

    # Set hyperparameters
    parms = {
        'population_size': 50,
        'generations': 5,
        'mu': 25,
        'lambda_': 50,
        'cxpb': 0.7,
        'mutpb': 0.2,
        'evcs_data': evcs_data,
        'EV_data': EV_data,
        'optimized_data_file': optimized_data_path
    }

    # Create the EVCS_Optimization object
    optimization = EVCS_Optimization(parms)

    # Run the optimization
    optimization.run()

if __name__ == "__main__":
    main()