import os
import requests
import csv


current_directory = os.getcwd()

# Define the relative path to the file
file_path = os.path.join(current_directory, "Datasets", "california_stations.csv")

url = "https://api.openchargemap.io/v3/poi"

# The parameters for the API request
params = {
    "key": "65480684-8133-4ba5-9289-949cc656022d",
    "countrycode": "US",
    "state": "California", 
    "maxresults": 100,
    "compact": True,
    "verbose": False,
}

response = requests.get(url, params=params)

def get_stations_data():
    # Open the CSV file for writing
    with open(file_path, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row to the CSV file
        writer.writerow(["Station Name", 
                        "Address",
                        "Status", 
                        "Waiting Time", 
                        "Type", 
                        "Coordinates", 
                        "Charging Type", 
                        "Power Level (kW)"])

        if response.status_code == 200:
            data = response.json()

            # Iterate through the stations
            for station in data:
                name = station.get("AddressInfo", {}).get("Title", "N/A")
                address = station.get("AddressInfo", {}).get("AddressLine1", "N/A")
                status = station.get("StatusType", {}).get("Title", "N/A")
                connector_type = station.get("Connections", [{}])[0].get("ConnectionType", {}).get("Title", "N/A")
                coordinates = f"{station.get('AddressInfo', {}).get('Latitude', 'N/A')}, {station.get('AddressInfo', {}).get('Longitude', 'N/A')}"
                
                # Get charging type
                charging_type = "N/A"
                if "Connections" in station:
                    for connection in station["Connections"]:
                        if "ChargingType" in connection and connection["ChargingType"]:
                            charging_type = connection["ChargingType"].get("Title", "N/A")
                            break  # Take the first valid charging type
                
                # Get power level (kW)
                power_level = "N/A"
                if "Connections" in station:
                    for connection in station["Connections"]:
                        if "PowerKW" in connection and connection["PowerKW"]:
                            power_level = connection.get("PowerKW", "N/A")
                            break  # Take the first valid power level

                # Get waiting time based on status
                if status == "Available":
                    waiting_time = "0 minutes"
                elif status == "In Use":
                    waiting_time = "10-30 minutes"
                elif status == "Out of Service":
                    waiting_time = "N/A"  # No wait time if out of service
                else:
                    waiting_time = "Unknown"  # If the status is unknown

                # Write station details
                writer.writerow([name, address, status, waiting_time, connector_type, coordinates, charging_type, power_level])

            print("Data successfully saved")
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


#
#main
def main():
    print("start")

if __name__=="__main__":
    main()
    get_stations_data()
