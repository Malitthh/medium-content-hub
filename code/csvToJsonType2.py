import csv
import json

# Increase the field size limit to a reasonably large value
csv.field_size_limit(1000000)  # You can adjust this value as needed

# Input and output file paths
input_csv_file = 'GOLDSET.csv'
output_json_file = 'Formatted_Output.json'

# Initialize a list to store the JSON objects
json_data = []

# Read data from the CSV file and convert it to JSON
with open(input_csv_file, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t')
    for row in csv_reader:
        json_object = {
            "articleText": row.get("articleText", ""),
            "sportsOutlet": "",
            "eventId": "",
            "leagueDivision": row.get("leagueDivision", ""),
            "playerName": "",
            "playerAge": row.get("playerAge", ""),
            "playerRank": row.get("playerRank", ""),
            "score": "",
            "playercountry": row.get("playercountry", ""),
            "playerID": row.get("playerID", ""),
            "teamID": row.get("teamID", ""),
            "teamName": row.get("teamName", ""),
            "teamDescription": row.get("teamDescription", "")
        }
        json_data.append(json_object)

# Write the JSON data to the output file
with open(output_json_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=2)

print(f"Data from '{input_csv_file}' has been converted and saved to '{output_json_file}'.")
