import csv
import json
import os

# Adjust the path to your CSV file
csv_file = './data/wellbeing_survey.csv'

# Read CSV data
data = []
with open(csv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # Read header
    for row in reader:
        record = {header[i]: row[i] for i in range(len(header))}
        data.append(record)

# Convert to JSON
json_data = json.dumps(data)

# Specify path to save data.json in a specific directory
json_file_path = './data/data.json'

# Ensure directory exists
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

# Write JSON data to file
with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file)

# Print success message
print(f"JSON file saved successfully at: {json_file_path}")
