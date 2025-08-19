import json
from collections import Counter

# Function to categorize content based on word count
def categorize_content(item):
    word_count = len(item["CONTENT"].split())
    if word_count <= 500:
        return "Small"
    elif word_count <= 1000:
        return "Medium"
    elif word_count <= 5000:
        return "Large"
    elif word_count <= 25000:
        return "XLarge"
    else:
        return "XXLarge"

# Load data from a JSON file
with open("XXLargewordformatted.json", "r") as file:
    data = json.load(file)

# Count categories
category_counts = Counter()

for item in data:
    category = categorize_content(item)
    item["CATEGORY"] = category
    category_counts[category] += 1

# Total records
total_records = len(data)

# Print summary with percentages
print("Summary of Categories:")
for category in ["Small", "Medium", "Large", "XLarge", "XXLarge"]:
    count = category_counts.get(category, 0)
    percentage = (count / total_records * 100) if total_records > 0 else 0
    print(f"{category}: {count} ({percentage:.2f}%)")

print(f"\nTotal records in file: {total_records}")
