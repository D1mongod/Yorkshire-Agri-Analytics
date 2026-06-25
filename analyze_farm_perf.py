import pandas as pd

print("--- Starting Yorkshire Farm Performance Analysis --- \n")

# 1. Load the generated CSV files into Pandas DataFrames
df_batches = pd.read_csv("farm_batches.csv")
df_weights = pd.read_csv("farm_weight_logs.csv")
df_feeds = pd.read_csv("farm_feed_logs.csv")

# 2. Let's look at the final weight of each batch at Week 20 (Market Ready Weight)
# We filter the data to see only week 20
final_weights = df_weights[df_weights["Week_Number"] == 20]
print("1. Final Average Weight per Batch at Week 20 (Target is ~110-115kg):")
print(final_weights[["Batch_ID", "Avg_Weight_kg"]])
print("-" * 50 + "\n")

# 3. Calculate total feed consumed by each batch to see expenses
# We group data by Batch_ID and sum the feed volume
total_feed = df_feeds.groupby("Batch_ID")["Feed_Consumed_kg"].sum().reset_index()

# 4. Merging weight data and feed data to calculate FCR (Feed Conversion Ratio)
# This is like VLOOKUP / XLOOKUP in Excel
summary_df = pd.merge(final_weights, total_feed, on="Batch_ID")

# Calculate overall weight gain per batch (Final weight minus starting 8kg)
summary_df["Total_Gain_per_Head_kg"] = summary_df["Avg_Weight_kg"] - 8.0

# Calculate Feed Conversion Ratio (FCR) for the whole cycle
# Formula: Total Feed Consumed / (Weight Gain * Number of Animals)
summary_df["Calculated_FCR"] = summary_df["Feed_Consumed_kg"] / (
    summary_df["Total_Gain_per_Head_kg"] * summary_df["Active_Head_Count"]
)

print("2. Operational KPI Summary Table (Look closely at Calculated_FCR):")
print(
    summary_df[
        [
            "Batch_ID",
            "Active_Head_Count",
            "Avg_Weight_kg",
            "Feed_Consumed_kg",
            "Calculated_FCR",
        ]
    ]
)
print("-" * 50 + "\n")

# 5. Automated Anomaly Detection
# In the UK, an FCR above 2.9 is a sign of financial loss. Let's flag it:
critical_fcr_threshold = 2.9
problematic_batches = summary_df[summary_df["Calculated_FCR"] > critical_fcr_threshold]

if not problematic_batches.empty:
    print("🚨 ALERT: CRITICAL EFFICIENCY LOSS DETECTED! 🚨")
    for index, row in problematic_batches.iterrows():
        print(
            f"Batch {row['Batch_ID']} has an alarming FCR of {row['Calculated_FCR']:.2f}! "
            f"They consumed {row['Feed_Consumed_kg']} kg of feed but only reached {row['Avg_Weight_kg']} kg."
        )
else:
    print("✅ All batches are performing within standard UK benchmarks.")