import stations
import data

def main():
    print("Fetch station data...")
    stations.get_stations_data() 

    print("Merege the data")
    data.merege_data()

if __name__ == "__main__":
    main()
