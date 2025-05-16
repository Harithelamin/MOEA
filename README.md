# MOEA
This project use Multi objective Evolutionary Algorithms for the Electric vehicle charging stand infrastructure problem

## Required Libraries

To run this project, you will need to install the following Python libraries:

- `pandas` - For data manipulation and analysis.
- `numpy` - For numerical computing.
- `matplotlib` - For plotting and visualizing data.
- `scikit-fuzzy` - For fuzzy logic operations and control systems.
- `seaborn` - For statistical data visualization used with `matplotlib`.
- `scikit-learn` - For machine learning tasks, such as metrics, and evaluation.
- `pickle` - For storing and opening dataset
- `nbimporter` - For importing Jupyter Notebooks as Python modules.
- `deap` - For Genetic Programming and implementing evolutionary algorithms.
- `pymoo` - For multi-objective optimization algorithms.


### Installation
You can install the required libraries using `pip`. Here is a sample installation command:

```bash
pip install pandas numpy matplotlib scikit-fuzzy seaborn scikit-learn nbimporter
```

## Run Steps 
1. Fetch and preprocess station data
    stations.main 
2. Fetch and preprocess EV data
    update_vehicles_with_coord.main 
3. Add coverage information to original station data
    add_coverage_to_station_data.main
4. Add distance information to original station data    
    add_distance_to_stations_data.main
5. Run NSGA-II optimization for EVCS
    nsga_II.main
6. Add coverage information to optimized station data
    add_coverage_to_optimized_data.main
7. Add distance information to optimized station data    
    add_distance_to_optimized_data.main
8. Calculate cost of original and optimized EVCS networks    
    calculate_evcs_cost.main

### Results
![alt text](Latex/Figures/evcs-nsga-flowchart.png)
![alt text](Latex/Figures/EVC_Levels.png)
![alt text](Latex/Figures/Pareto_Front.png)
![alt text](Latex/Figures/Trade_Off.png)
![alt text](Latex/Figures/original_map.PNG)
![alt text](Latex/Figures/optimized_map.PNG)
![alt text](Latex/Figures/ev_distance.png)
![alt text](Latex/Figures/distance.png)
![alt text](Latex/Figures/Original_vs_Optimized_evcs_network.png)
![alt text](Latex/Figures/Original_vs_Optimized_evcs_chargers_number.png)
![alt text](Latex/Figures/Original_vs_Optimized_evcs_chargers_speed.png)
![alt text](Latex/Figures/plot_EVCS_cost.png)


