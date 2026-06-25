import os
import random
from datetime import datetime, timedelta
import pandas as pd


def generate_data():
    print("Launching data generator for Yorkshire Agri-Farm Ltd...")

    # 1. Generate livestock batches metadata
    batches = []
    start_date = datetime(2026, 1, 1)

    for i in range(1, 6):  # Generating 5 distinct animal groups
        batch_id = f"UK-2026-B{i:02d}"
        # Batches arrive with a 2-week interval
        b_date = start_date + timedelta(days=(i - 1) * 14)
        head_count = random.randint(180, 220)  # Standard batch size around 200

        batches.append(
            {
                "Batch_ID": batch_id,
                "Arrival_Date": b_date.strftime("%Y-%m-%d"),
                "Initial_Head_Count": head_count,
                "Breed": "Yorkshire X Landrace",
            }
        )

    df_batches = pd.DataFrame(batches)

    # 2. Generate weight logs and feed consumption tracking
    weight_logs = []
    feed_logs = []

    for batch in batches:
        b_id = batch["Batch_ID"]
        current_date = datetime.strptime(batch["Arrival_Date"], "%Y-%m-%d")
        current_weight = 8.0  # Initial weight at weaning/wean-to-finish entry (8 kg)
        head_count = batch["Initial_Head_Count"]

        # Standard feeding cycle lasts 20 weeks (approx. 140 days)
        for week in range(1, 21):
            current_date += timedelta(days=7)

            # Biological growth logic: Average Daily Gain (ADG) increases with age
            if week < 6:
                daily_gain = random.uniform(0.45, 0.52)  # Starter phase
            elif week < 13:
                daily_gain = random.uniform(0.70, 0.78)  # Grower phase
            else:
                daily_gain = random.uniform(0.82, 0.92)  # Finisher phase

            # Injecting an anomaly into Batch 3 for future analytics practice
            # This batch performs worse due to simulated health/feed issues
            if b_id == "UK-2026-B03":
                daily_gain -= 0.08

            weight_gain_week = daily_gain * 7
            current_weight += weight_gain_week

            # Append weekly weight records
            weight_logs.append(
                {
                    "Log_Date": current_date.strftime("%Y-%m-%d"),
                    "Batch_ID": b_id,
                    "Week_Number": week,
                    "Avg_Weight_kg": round(current_weight, 2),
                    "Active_Head_Count": head_count,
                }
            )

            # Calculate feed consumption based on Feed Conversion Ratio (FCR)
            # Standard UK FCR baseline is around 2.6. Batch 3 has a poor FCR of 3.1
            fcr_base = 2.6 if b_id != "UK-2026-B03" else 3.1
            total_feed_chunk = weight_gain_week * fcr_base * head_count

            feed_logs.append(
                {
                    "Log_Date": current_date.strftime("%Y-%m-%d"),
                    "Batch_ID": b_id,
                    "Feed_Type": (
                        "Starter"
                        if week < 6
                        else "Grower" if week < 13 else "Finisher"
                    ),
                    "Feed_Consumed_kg": round(total_feed_chunk, 1),
                }
            )

    df_weights = pd.DataFrame(weight_logs)
    df_feeds = pd.DataFrame(feed_logs)

    # Save dataframes to raw CSV files
    df_batches.to_csv("farm_batches.csv", index=False)
    df_weights.to_csv("farm_weight_logs.csv", index=False)
    df_feeds.to_csv("farm_feed_logs.csv", index=False)

    print(
        "Success! Generated files: farm_batches.csv, farm_weight_logs.csv, farm_feed_logs.csv"
    )


if __name__ == "__main__":
    generate_data()