import json

# Load the unformatted JSON file
# if input file on the same file, file name should be enough
with open('XXLargewordcount.json', 'r') as unformatted_file:
    data = json.load(unformatted_file)

# Write the formatted JSON to a new file
with open('Formatted.json', 'w') as formatted_file:
    json.dump(data, formatted_file, indent=4, sort_keys=True)

print("Formatted JSON written to 'Formatted.json'")