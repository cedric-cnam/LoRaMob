import os
import csv

# Define the folder where the individual CSV files are located
output_folder = "d:\Analysis\CSV"
combined_csv_file = "json_to_csv_data.csv"

# List all files in the Output folder that end with .csv
csv_files = [f for f in os.listdir(output_folder) if f.endswith('.csv')]

# Open the combined CSV file for writing
with open(combined_csv_file, 'w', newline='') as combined_file:
    writer = None  # Initialize writer as None; it will be set on the first file

    # Iterate over each CSV file
    for csv_file in csv_files:
        csv_file_path = os.path.join(output_folder, csv_file)
        
        # Open each individual CSV file
        with open(csv_file_path, 'r') as f:
            reader = csv.DictReader(f)
            
            # Initialize the writer with the field names from the first file
            if writer is None:
                writer = csv.DictWriter(combined_file, fieldnames=reader.fieldnames)
                writer.writeheader()  # Write header only once at the beginning

            # Write each row from the current CSV file to the combined file
            for row in reader:
                writer.writerow(row)

print(f"All CSV files have been combined into {combined_csv_file}")
