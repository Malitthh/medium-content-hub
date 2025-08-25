import json
import csv

def analyze_results(json_file):
    try:
        # Try with utf-8 first
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except UnicodeDecodeError:
        print("UTF-8 failed, trying UTF-16...")
        with open(json_file, 'r', encoding='utf-16') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Validate structure
    if not isinstance(data, dict) or 'results' not in data:
        print("Invalid JSON structure: expected a dictionary with 'results' key.")
        return

    results = data['results']
    total_count = len(results)

    completed_count = 0
    completed_with_results_count = 0
    error_count = 0
    error_ids = []

    for result in results:
        if isinstance(result, dict):
            status = result.get('status', '')
            request_id = result.get('requestId', 'N/A')

            if status == 'Completed':
                completed_count += 1
                if result.get('result') and isinstance(result['result'], list) and result['result']:
                    completed_with_results_count += 1
            elif status == 'Error':
                error_count += 1
                error_ids.append(request_id)

    # Percentages (avoid division by zero)
    completed_percent = (completed_count / total_count * 100) if total_count else 0
    error_percent = (error_count / total_count * 100) if total_count else 0

    # Save summary to CSV
    with open("Results_Summary.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total objects", total_count])
        writer.writerow(["Completed", f"{completed_count} ({completed_percent:.2f}%)"])
        writer.writerow(["Completed with non-empty results", completed_with_results_count])
        writer.writerow(["Error", f"{error_count} ({error_percent:.2f}%)"])

        # Empty line then errors
        writer.writerow([])
        writer.writerow(["Error Request IDs"])
        for eid in error_ids:
            writer.writerow([eid])

    print("Processing complete! Results saved to 'Results_Summary.csv'.")

# Run
json_file_path = 'DataOutput.json'
analyze_results(json_file_path)
