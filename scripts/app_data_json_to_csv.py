import os
import json
import csv

# Define the path to the APP_Data and destination folder
app_data_folder = "11-Days\Data\APP_Data"
destination_folder = "11-Days\Data\CSV"

# Function to recursively flatten JSON
def flatten_json(data, prefix=''):
    flattened_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            flattened_data.update(flatten_json(value, prefix + key + '_'))
        else:
            flattened_data[prefix + key] = value
    return flattened_data

# Function to extract relevant information from the line
def extract_info(line):
    parts = line.split(' ', 1)
    event_info = parts[0].split('/')[-1]
    data = json.loads(parts[1])
    rx_info = data.pop('rxInfo', [])

    flattened_data = flatten_json(data)

    formatted_data = []
    for rx in rx_info:
        rx_data = flatten_json(rx, 'rxInfo_')
        formatted_rx = {'event_info': event_info, **flattened_data, **rx_data}
        formatted_data.append(formatted_rx)

    return formatted_data

# Function to convert JSON data to CSV format
def app_data_json_to_csv(file_path, csv_file_path):
    # Open CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = None
        writer = None

        # Open the JSON file and process each line
        with open(file_path, 'r') as file:
            for line in file:
                # Extract data and skip the line if extraction fails or returns empty
                formatted_data = extract_info(line.strip())
                
                if not formatted_data:
                    # Skip this line if no data is extracted
                    continue

                # Initialize CSV writer and write header if not initialized yet
                if not writer:
                    fieldnames = formatted_data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                # Write each formatted data row to CSV
                for data in formatted_data:
                    writer.writerow(data)

    print("Data has been saved to", csv_file_path)


# List all files in the APP_Data folder
files = os.listdir(app_data_folder)

# Filter out only JSON files
json_files = [f for f in files if f.endswith('.json')]

# Create a new list with '.csv' instead of '.json'
csv_list = [f.replace('.json', '.csv') for f in json_files]

# Combine the folder path with each file name
json_files = [os.path.join(app_data_folder, f) for f in json_files]


# Combine the folder path with each file name
csv_list = [os.path.join(destination_folder, f) for f in csv_list]

# # Print the list of JSON files
# print("List of JSON files:", json_files)

# # Print the list of CSV files
# print("List of CSV files:", csv_list)


print("Count Json Files: ", len(json_files))
print("Count CSV Files: ", len(csv_list))


for i in range(len(json_files)):  
    print("Count: ", i)
    print("Current Json File: ", json_files[i])
    print("Current CSV File: ", csv_list[i])
    app_data_json_to_csv(json_files[i], csv_list[i])
