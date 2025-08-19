import pandas as pd
print(pd.__version__)
import csv

# Increase field size limit to handle large cells
csv.field_size_limit(2_000_000)

# Define the CSV file path
csv_file = "GOLDSET.csv"

# Use ONLY this - do NOT include error_bad_lines or warn_bad_lines
try:
    df = pd.read_csv(csv_file, encoding="utf-8", on_bad_lines='skip', engine="python")
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit()

# Print actual column names
print("Actual column names in CSV:")
print(df.columns.tolist())

# Define expected columns
columns_to_extract = [
    "ARTICLE_ID", "CATEGORY_ID", "BODY_TEXT", "HEADLINE_TEXT",
    "BODY_TRANSLATED", "HEADLINE_TRANSLATED", "SOURCE_URL", "IMPORT_DATE",
    "AUTHOR_NAME", "AUTHOR_ID", "LOCATION_NAME", "LOCATION_ID",
    "LANGUAGE_ORIGINAL"
]

# Check for missing columns
missing_columns = [col for col in columns_to_extract if col not in df.columns]
if missing_columns:
    print(f"Missing columns in CSV: {missing_columns}")
else:
    print("All expected columns found!")

# Keep only valid columns
df = df[[col for col in columns_to_extract if col in df.columns]]

# Save cleaned CSV
clean_csv_file = "Cleaned_GOLDSET.csv"
df.to_csv(clean_csv_file, index=False)

# Convert to JSON
output_json_file = "JSONOutput.json"
df.to_json(output_json_file, orient="records", indent=4)

print(f"Cleaned CSV saved as {clean_csv_file}")
print(f"JSON output saved as {output_json_file}")
