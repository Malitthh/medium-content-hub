import json

def count_completed_and_non_empty_results(json_file):
    # Initialize counters
    completed_count = 0
    completed_with_results_count = 0

    # Try opening the file with different encodings
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except UnicodeDecodeError:
        print("UTF-8 encoding failed, trying with UTF-16 encoding...")
        with open(json_file, 'r', encoding='utf-16') as file:
            data = json.load(file)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # Print the keys of the outer dictionary to understand its structure
    if isinstance(data, dict):
        print(f"Data is a dictionary. Keys: {data.keys()}")
    else:
        print(f"Data is not a dictionary, it's a {type(data)}")
        return

    # Check if 'results' is the key containing the list of results
    if 'results' in data:
        results = data['results']
        print(f"First result in 'results' list: {results[0]}")
    else:
        print("The expected key 'results' is not present in the data.")
        return

    # Now iterate through the 'results' list
    for result in results:
        # Ensure each result is a dictionary and contains the key 'status'
        if isinstance(result, dict) and 'status' in result:
            if result['status'] == 'COMPLETED':
                completed_count += 1
                # Check if 'result' is not empty
                if result.get('result') and isinstance(result['result'], list) and result['result']:
                    completed_with_results_count += 1
        else:
            print(f"Skipping invalid result: {result}")
    
    # Output the counts to a text file
    with open("Completed Count.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(f"Total completed: {completed_count}\n")
        output_file.write(f"Completed with non-empty results: {completed_with_results_count}\n")
    
    print("Processing complete! Results saved to 'output_count.txt'.")

# Replace 'your_json_file.json' with the path to your actual JSON file
json_file_path = 'LatestDataAllOutput.json'
count_completed_and_non_empty_results(json_file_path)
