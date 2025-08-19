import json
import uuid

def is_valid_content(item):
    """
    Check if the item has all required fields and is valid.
    """
    required_fields = ["articleText", "sportsOutlet", "eventId", "leagueDivision"]
    
    # Check if all required fields are present and non-empty
    for field in required_fields:
        if not item.get(field):
            return False  # Invalid if any required field is missing or empty
    
    return True

def filter_us_data(data):
    """
    Filter the data to keep only U.S. jurisdiction items.
    """
    us_jurisdictions = ["United States of America", "US", "United States"]  # List of variations to match
    filtered_data = [item for item in data if item.get("leagueDivision") in us_jurisdictions]
    
    return filtered_data

def process_and_format_json(input_file, output_file):
    # Load the input data from the JSON file
    with open(input_file, 'r') as infile:
        input_data = json.load(infile)
    
    # Filter out invalid content
    valid_data = [item for item in input_data if is_valid_content(item)]
    
    # Filter for U.S. jurisdiction
    us_data = filter_us_data(valid_data)
    
    # Save the filtered data to the output JSON file
    with open(output_file, 'w') as outfile:
        json.dump(us_data, outfile, indent=4)

# Example usage
input_json_file = 'output.json'  # Replace with the path to your input JSON file (the one generated from previous script)
output_json_file = 'filtered_outputus1.json'  # Replace with the desired output JSON file path

process_and_format_json(input_json_file, output_json_file)
