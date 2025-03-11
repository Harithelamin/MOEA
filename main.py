import stations
import data
import plotting_EVCS

def main():
    print("Fetch station data...")
    stations.get_stations_data() 

    print("Merege the data")
    data.merege_data()

    print("Ploatin EVCS")
    plotting_EVCS.ploatin_EVCS

if __name__ == "__main__":
    main()
