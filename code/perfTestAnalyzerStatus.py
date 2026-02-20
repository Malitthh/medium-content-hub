import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Load CSV or Excel file (NO FILTERING)
input_file = "sample.csv"

if input_file.lower().endswith(".csv"):
    df_all = pd.read_csv(input_file, encoding_errors="ignore")
elif input_file.lower().endswith((".xls", ".xlsx")):
    df_all = pd.read_excel(input_file)
else:
    raise ValueError("Unsupported file format.")

df_all.columns = df_all.columns.str.strip()
base_filename = os.path.splitext(os.path.basename(input_file))[0]

# True total requests (anchor metric)
total_requests = len(df_all)

# Step 2: Parse durations (non-destructive)
def parse_duration(val):
    try:
        minutes, seconds = str(val).split(":")
        return float(minutes) * 60 + float(seconds)
    except:
        return None

df_all["created_sec"] = df_all["created"].apply(parse_duration)
df_all["updated_sec"] = df_all["updated"].apply(parse_duration)

# Step 3: Calculate duration (do NOT drop rows)
df_all["duration_sec"] = df_all["updated_sec"] - df_all["created_sec"]

# Step 4: Status counts (from TOTAL requests)
status_counts = df_all["status"].value_counts(dropna=False)

completed_count   = status_counts.get("COMPLETED", 0)
accepted_count    = status_counts.get("ACCEPTED", 0)
in_progress_count = status_counts.get("IN_PROGRESS", 0)
received_count    = status_counts.get("RECEIVED", 0)
error_count       = status_counts.get("ERROR", 0)

known_status_total = (
    completed_count +
    accepted_count +
    in_progress_count +
    received_count +
    error_count
)

other_status_count = total_requests - known_status_total

# Step 4.1: Error calculations (still from TOTAL)
error_status_count = error_count

error_timeout_count = df_all[
    (df_all["duration_sec"].notna()) &
    (df_all["duration_sec"] > 300)
].shape[0]

combined_error_mask = (
    (df_all["status"] == "ERROR") |
    (
        df_all["duration_sec"].notna() &
        (df_all["duration_sec"] > 300)
    )
)

error_combined_count = combined_error_mask.sum()

error_status_rate = (error_status_count / total_requests) * 100
error_timeout_rate = (error_timeout_count / total_requests) * 100
error_combined_rate = (error_combined_count / total_requests) * 100

# Step 4.2: Completed requests (definition unchanged)
df_completed = df_all[~df_all["status"].isin(["IN_PROGRESS", "ACCEPTED", "ERROR"])]

completed_requests = len(df_completed)
completed_percentage = (completed_requests / total_requests) * 100

# Step 4.3.1: Valid completed requests (timing math ONLY)
df_valid = df_completed[
    (df_completed["duration_sec"].notna()) &
    (df_completed["duration_sec"] >= 0)
]

avg_duration_sec = df_valid["duration_sec"].mean()
variance = df_valid["duration_sec"].var(ddof=0)
std_dev = df_valid["duration_sec"].std(ddof=0)
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

# Step 4.4: Observation window (valid completed only)
window_start = df_valid["created_sec"].min()
window_end = df_valid["updated_sec"].max()
total_observation_time_sec = window_end - window_start

if total_observation_time_sec <= 0:
    raise ValueError("Invalid observation window")

# Step 4.5: Arrival rate λ (Little’s Law)
arrival_rate = completed_requests / total_observation_time_sec
L = arrival_rate * avg_duration_sec if avg_duration_sec else 0

# Step 5: Console output
print("\n--- System Summary ---")
print(f"Total Requests Sent: {total_requests}")
print(f"Completed Requests: {completed_requests} ({completed_percentage:.2f}%)")
print(f"Average Response Time (sec): {avg_duration_sec:.2f}")
print(f"Std Dev (sec): {std_dev:.2f}")
print(f"CV: {cv:.3f} → {stability}")

print("\n--- Little’s Law ---")
print(f"Observation Window (sec): {round(total_observation_time_sec, 2)}")
print(f"Arrival Rate λ (req/sec): {arrival_rate:.4f}")
print(f"Average Time W (sec): {round(avg_duration_sec, 2)}")
print(f"Average Concurrency L: {round(L, 2)}")

# Step 6: Summary DataFrame
summary_df = pd.DataFrame({
   "Metric": [
       "Total Requests",

       "Processed Requests",
       "Accepted Requests",
       "In Progress Requests",
       "Received Requests",
       "Error Requests",
       "Other / Unknown Status Requests",

       "Completed Requests",
       "Completed Requests (%)",

       "Error Requests (Status)",
       "Error Rate (Status) (%)",
       "Error Requests (Timeout >5min)",
       "Error Rate (Timeout) (%)",
       "Error Requests (Combined)",
       "Error Rate (Combined) (%)",

       "Average Response Time (s)",
       "Variance (σ²)",
       "Standard Deviation (σ)",
       "Coefficient of Variation (CV)",
       "System Stability",
       "Arrival Rate λ (req/sec)",
       "Little’s Law (L = λ × W)"
   ],
   "Value": [
       total_requests,

       completed_count,
       accepted_count,
       in_progress_count,
       received_count,
       error_count,
       other_status_count,

       completed_requests,
       f"{completed_percentage:.2f}%",

       error_status_count,
       f"{error_status_rate:.2f}%",
       error_timeout_count,
       f"{error_timeout_rate:.2f}%",
       error_combined_count,
       f"{error_combined_rate:.2f}%",

       round(avg_duration_sec, 2),
       round(variance, 2),
       round(std_dev, 2),
       round(cv, 3),
       stability,
       round(arrival_rate, 4),
       round(L, 2)
   ]
})

# Step 7: Save Excel output
excel_output = f"{base_filename}_with_duration_summary.xlsx"
with pd.ExcelWriter(excel_output) as writer:
    df_all.to_excel(writer, sheet_name="All Requests", index=False)
    df_valid.to_excel(writer, sheet_name="Completed Requests", index=False)
    summary_df.to_excel(writer, sheet_name="Summary", index=False)

print(f"\nSaved Excel report: {excel_output}")

# Step 8: Percentiles chart
percentile_values = df_valid["duration_sec"].quantile(
    [0.01, 0.05, 0.10, 0.25, 0.50, 0.80, 0.95, 0.99]
)
percentile_values.index = ["1st", "5th", "10th", "25th", "50th", "80th", "95th", "99th"]

plt.figure(figsize=(8, 5))
ax = percentile_values.plot(kind="bar", color="#00ADB5", edgecolor="black")
plt.title("Job Process Time Percentiles (Completed Requests)")
plt.ylabel("Duration (seconds)")
plt.grid(axis="y", linestyle="--", alpha=0.7)

for i, value in enumerate(percentile_values):
    ax.text(i, value * 1.02, f"{value:.2f}s", ha="center", va="bottom")

plt.tight_layout()
plt.savefig(f"{base_filename}_percentile_chart.png")
plt.close()

# Step 9: Mean vs Std Dev chart
plt.figure(figsize=(6, 5))
bars = plt.bar(
    ["Mean (μ)", "Std Dev (σ)"],
    [avg_duration_sec, std_dev],
    color=["#0077b6", "#ffb703"],
    edgecolor="black"
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() * 1.02,
        f"{bar.get_height():.2f}",
        ha="center"
    )

plt.text(
    0.5,
    max(avg_duration_sec, std_dev) * 0.85,
    f"CV = {cv:.3f}\n{stability}",
    ha="center",
    bbox=dict(boxstyle="round", fc="lightyellow")
)

plt.tight_layout()
plt.savefig(f"{base_filename}_mean_vs_stddev.png")
plt.close()