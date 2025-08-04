import pandas as pd 
import matplotlib.pyplot as plt
import os

# Step 1: Load CSV without datetime parsing
input_file = "1110.csv"
df = pd.read_csv(input_file)
df.columns = df.columns.str.strip()  # Remove any whitespace around headers

# Extract base name without extension (e.g., "1110")
base_filename = os.path.splitext(os.path.basename(input_file))[0]

# Step 2: Helper to convert MM:SS.s format to total seconds
def parse_duration(duration_str):
    try:
        minutes, seconds = duration_str.split(":")
        return float(minutes) * 60 + float(seconds)
    except:
        return None  # Return None for invalid or missing data

# Step 3: Convert 'created' and 'updated' columns to seconds
df["created_sec"] = df["created"].apply(parse_duration)
df["updated_sec"] = df["updated"].apply(parse_duration)

# Step 4: Calculate duration
df["duration_sec"] = df["updated_sec"] - df["created_sec"]
df = df[df["duration_sec"] >= 0]  # Filter valid durations

# Step 5: Count how many exceed 300s
count_exceed_300s = (df["duration_sec"] > 300).sum()
total_requests = len(df)

print("Total Requests:", total_requests)
print("Requests > 300s:", count_exceed_300s)

# Step 6: Prepare summary DataFrame
summary_df = pd.DataFrame({
    "Metric": ["Total Requests", "Requests > 300s"],
    "Value": [total_requests, count_exceed_300s]
})

# Step 7: Export both sheets to Excel
excel_output = f"{base_filename}_with_duration_summary.xlsx"
with pd.ExcelWriter(excel_output) as writer:
    df.to_excel(writer, sheet_name="Processed Data", index=False)
    summary_df.to_excel(writer, sheet_name="Summary", index=False)

# Step 8: Generate percentile values
percentile_values = df["duration_sec"].quantile([0.01, 0.05, 0.10, 0.25, 0.50, 0.80, 0.95, 0.99])
percentile_values.index = ["1st", "5th", "10th", "25th", "50th", "80th", "95th", "99th"]

# Step 9: Plot the percentile chart
plt.figure(figsize=(8, 5))
percentile_values.plot(kind="bar", color="#00ADB5", edgecolor="black")

plt.title("Job Process Time Percentiles (in seconds)", fontsize=14)
plt.ylabel("Duration (seconds)")
plt.xlabel("Percentile")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Step 10: Save and show the chart
chart_output = f"{base_filename}_percentile_chart.png"
plt.savefig(chart_output)
plt.show()
