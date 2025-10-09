import pandas as pd  
import matplotlib.pyplot as plt
import os

# Step 1: Load CSV or Excel file
input_file = "sample.csv"  # Change to your file path here

if input_file.lower().endswith(".csv"):
    df_raw = pd.read_csv(input_file)
elif input_file.lower().endswith((".xls", ".xlsx")):
    df_raw = pd.read_excel(input_file)
else:
    raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

df_raw.columns = df_raw.columns.str.strip()

# Extract base name without extension
base_filename = os.path.splitext(os.path.basename(input_file))[0]

# Step 2: Convert duration to seconds
def parse_duration(duration_str):
    try:
        minutes, seconds = duration_str.split(":")
        return float(minutes) * 60 + float(seconds)
    except:
        return None

df_raw["created_sec"] = df_raw["created"].apply(parse_duration)
df_raw["updated_sec"] = df_raw["updated"].apply(parse_duration)

# Step 3: Calculate duration
df_raw["duration_sec"] = df_raw["updated_sec"] - df_raw["created_sec"]
df_raw = df_raw[df_raw["duration_sec"] >= 0]

# Total requests before filtering
total_requests_before_filter = len(df_raw)

# STEP 4.6: Error Rate Calculations
error_status_count = (df_raw['status'] == 'ERROR').sum()
error_status_rate = (error_status_count / total_requests_before_filter) * 100 if total_requests_before_filter else 0

error_timeout_count = (df_raw['duration_sec'] > 300).sum()
error_timeout_rate = (error_timeout_count / total_requests_before_filter) * 100 if total_requests_before_filter else 0

error_combined_count = ((df_raw['status'] == 'ERROR') | (df_raw['duration_sec'] > 300)).sum()
error_combined_rate = (error_combined_count / total_requests_before_filter) * 100 if total_requests_before_filter else 0

print(f"Error Rate (Status): {error_status_count} → {error_status_rate:.2f}%")
print(f"Error Rate (Timeout > 5min): {error_timeout_count} → {error_timeout_rate:.2f}%")
print(f"Error Rate (Combined): {error_combined_count} → {error_combined_rate:.2f}%")

# Step 4.7: Filter for successful requests only
df = df_raw[~df_raw['status'].isin(['IN_PROGRESS', 'ACCEPTED', 'ERROR'])]

# Completed requests & stats
completed_requests = len(df)
completed_percentage = (completed_requests / total_requests_before_filter) * 100

count_exceed_300s = (df["duration_sec"] > 300).sum()
avg_duration_sec = df["duration_sec"].mean()
variance = df["duration_sec"].var(ddof=0)
std_dev = df["duration_sec"].std(ddof=0)
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

arrival_rate = float(input("Enter arrival rate (req/sec): "))
L = arrival_rate * avg_duration_sec if avg_duration_sec else 0

print("Total Requests:", total_requests_before_filter)
print("Completed Requests:", completed_requests)
print(f"Completed Requests %: {completed_percentage:.2f}%")
print("Requests > 300s:", count_exceed_300s)
print("Average Response Time (seconds):", round(avg_duration_sec, 2))
print("Variance (σ²):", round(variance, 2))
print("Standard Deviation (σ):", round(std_dev, 2))
print("Little's Law (L = λ × W):", round(L, 2))

avg_minutes = int(avg_duration_sec // 60)
avg_seconds = avg_duration_sec % 60
print(f"Average Response Time (MM:SS.s): {avg_minutes}:{avg_seconds:.2f}")

# Step 6: Summary DataFrame
summary_df = pd.DataFrame({
    "Metric": [
        "Total Requests",
        "Completed Requests",
        "Completed Requests (%)",
        "Error Requests (Status)",
        "Error Rate (Status) (%)",
        "Error Requests (Timeout >5min)",
        "Error Rate (Timeout) (%)",
        "Error Requests (Combined)",
        "Error Rate (Combined) (%)",
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
        error_status_count,
        f"{error_status_rate:.2f}%",
        error_timeout_count,
        f"{error_timeout_rate:.2f}%",
        error_combined_count,
        f"{error_combined_rate:.2f}%",
        count_exceed_300s,
        round(avg_duration_sec, 2),
        round(variance, 2),
        round(std_dev, 2),
        round(cv, 3) if cv is not None else "N/A",
        stability,
        round(L, 2)
    ]
})


excel_output = f"{base_filename}_with_duration_summary.xlsx"
with pd.ExcelWriter(excel_output) as writer:
    df.to_excel(writer, sheet_name="Processed Data", index=False)
    summary_df.to_excel(writer, sheet_name="Summary", index=False)

# Step 8: Percentiles
percentile_values = df["duration_sec"].quantile([0.01, 0.05, 0.10, 0.25, 0.50, 0.80, 0.95, 0.99])
percentile_values.index = ["1st", "5th", "10th", "25th", "50th", "80th", "95th", "99th"]

# Step 9: Percentile Chart
plt.figure(figsize=(8, 5))
percentile_values.plot(kind="bar", color="#00ADB5", edgecolor="black")
plt.title("Job Process Time Percentiles (Completed Requests)", fontsize=14)
plt.ylabel("Duration (seconds)")
plt.xlabel("Percentile")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
chart_output = f"{base_filename}_percentile_chart.png"
plt.savefig(chart_output)
print(f"Saved percentile chart: {chart_output}")
plt.close()

# Step 10: Mean vs Std Dev Chart
plt.figure(figsize=(6, 5))
bars = plt.bar(
    ["Mean (μ)", "Std Dev (σ)"],
    [avg_duration_sec, std_dev],
    color=["#3fa4db", "#79ff5e"],
    edgecolor="black"
)

plt.title("Mean vs Standard Deviation", fontsize=14)
plt.ylabel("Duration (seconds)")
plt.grid(axis="y", linestyle="--", alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + (0.02 * height),
             f"{height:.2f}", ha='center', va='bottom', fontsize=10)

plt.text(0.5, max(avg_duration_sec, std_dev) * 0.9,
         f"CV = {cv:.3f} → {stability}",
         ha="center", va="center", fontsize=12,
         bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="black"))

plt.tight_layout()
deviation_chart_output = f"{base_filename}_mean_vs_stddev.png"
plt.savefig(deviation_chart_output)
print(f"Saved deviation chart: {deviation_chart_output}")
plt.close()

# Options: "status" | "timeout" | "combined"
error_mode = "combined"  

if error_mode == "status":
    error_count = error_status_count
    error_label = "Error (Status)"
elif error_mode == "timeout":
    error_count = error_timeout_count
    error_label = "Error (Timeout >5min)"
else:
    error_count = error_combined_count
    error_label = "Error (Combined)"

plt.figure(figsize=(5, 5))
labels = ['Success', error_label]
sizes = [total_requests_before_filter - error_count, error_count]
colors = ['#4CAF50', '#FF4C4C']

plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
plt.title(f'Success vs {error_label}', fontsize=14)
plt.tight_layout()

error_chart_output = f"{base_filename}_error_rate_{error_mode}.png"
plt.savefig(error_chart_output)
print(f"Saved error rate pie chart: {error_chart_output}")
plt.close()
