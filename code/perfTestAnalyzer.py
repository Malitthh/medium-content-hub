import pandas as pd  
import matplotlib.pyplot as plt
import os

# Step 1: Load CSV or Excel file without datetime parsing
input_file = "20req1.csv"  # Change to your input file path here

if input_file.lower().endswith(".csv"):
    df = pd.read_csv(input_file)
elif input_file.lower().endswith((".xls", ".xlsx")):
    df = pd.read_excel(input_file)
else:
    raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

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

# Save total requests before filtering
total_requests_before_filter = len(df)

# Step 4.5: Filter out unwanted statuses (exclude IN_PROGRESS and ACCEPTED)
df = df[~df['status'].isin(['IN_PROGRESS', 'ACCEPTED', 'ERROR'])]

# Completed requests count & percentage
completed_requests = len(df)
completed_percentage = (completed_requests / total_requests_before_filter) * 100

# Step 5: Count how many exceed 300s
count_exceed_300s = (df["duration_sec"] > 300).sum()

# Step 5.1: Calculate average response time
avg_duration_sec = df["duration_sec"].mean()

# Step 5.2: Variance & Standard Deviation
variance = df["duration_sec"].var(ddof=0)  # Population variance
std_dev = df["duration_sec"].std(ddof=0)   # Population standard deviation

# Step 5.3: Coefficient of Variation (CV = σ / μ)
cv = std_dev / avg_duration_sec if avg_duration_sec else None

# Stability interpretation
if cv is not None:
    if cv < 0.1:
        stability = "Very Stable"
    elif cv <= 0.3:
        stability = "Acceptable Variance"
    else:
        stability = "Unstable / Unpredictable"
else:
    stability = "N/A"

print("Coefficient of Variation (CV):", round(cv, 3))
print("System Stability:", stability)

# Step 5.4: Little's Law
arrival_rate = float(input("Enter arrival rate (req/sec): "))  # user input
L = arrival_rate * avg_duration_sec if avg_duration_sec else 0

# Console output
print("Total Requests:", total_requests_before_filter)
print("Completed Requests:", completed_requests)
print(f"Completed Requests %: {completed_percentage:.2f}%")
print("Requests > 300s:", count_exceed_300s)
print("Average Response Time (seconds):", round(avg_duration_sec, 2))
print("Variance (σ²):", round(variance, 2))
print("Standard Deviation (σ):", round(std_dev, 2))
print("Little's Law (L = λ × W):", round(L, 2))

# Also print average time as MM:SS.s
avg_minutes = int(avg_duration_sec // 60)
avg_seconds = avg_duration_sec % 60
print(f"Average Response Time (MM:SS.s): {avg_minutes}:{avg_seconds:.2f}")

# Step 6: Prepare summary DataFrame including average duration, variance, std dev, and Little’s Law
summary_df = pd.DataFrame({
    "Metric": [
        "Total Requests",
        "Completed Requests",
        "Completed Requests (%)",
        "Requests > 300s",
        "Average Response Time (s)",
        "Variance (σ²)",
        "Standard Deviation (σ)",
        "Coefficient of Variation (CV)",
        "System Stability",
        "Little’s Law (L = λ × W)"
    ],
    "Value": [
        total_requests_before_filter,
        completed_requests,
        f"{completed_percentage:.2f}%",
        count_exceed_300s,
        round(avg_duration_sec, 2),
        round(variance, 2),
        round(std_dev, 2),
        round(cv, 3) if cv is not None else "N/A",
        stability,
        round(L, 2)
    ]
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

plt.title("Job Process Time Percentiles (Completed Requests)", fontsize=14)
plt.ylabel("Duration (seconds)")
plt.xlabel("Percentile")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Save percentile chart
chart_output = f"{base_filename}_percentile_chart.png"
plt.savefig(chart_output)
print(f"Saved percentile chart: {chart_output}")
plt.close()  # close so next plot doesn't overwrite

# Step 10: Plot Mean vs Std Dev with CV annotation
plt.figure(figsize=(6, 5))
bars = plt.bar(
    ["Mean (μ)", "Std Dev (σ)"],
    [avg_duration_sec, std_dev],
    color=["#0077b6", "#ffb703"],
    edgecolor="black"
)

plt.title("Mean vs Standard Deviation", fontsize=14)
plt.ylabel("Duration (seconds)")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Annotate bar values
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + (0.02 * height),
             f"{height:.2f}", ha='center', va='bottom', fontsize=10)

# Add CV annotation
plt.text(0.5, max(avg_duration_sec, std_dev) * 0.9,
         f"CV = {cv:.3f} → {stability}",
         ha="center", va="center", fontsize=12,
         bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="black"))

plt.tight_layout()

# Save deviation chart
deviation_chart_output = f"{base_filename}_mean_vs_stddev.png"
plt.savefig(deviation_chart_output)
print(f"Saved deviation chart: {deviation_chart_output}")
plt.close()
