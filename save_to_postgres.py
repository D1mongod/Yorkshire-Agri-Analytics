import pandas as pd
from sqlalchemy import create_engine

print("--- Launching PostgreSQL Migration for Yorkshire Farm --- \n")

# 1. Connection string for PostgreSQL: 'postgresql://username:password@host:port/database_name'
# Replace 'your_password' with your actual pgAdmin/Postgres password!
db_url = "postgresql://postgres:34523452@localhost:5432/yorkshire_farm"

try:
    # Create the connection engine
    engine = create_engine(db_url)

    # 2. Load clean CSV files into Pandas
    df_batches = pd.read_csv("farm_batches.csv")
    df_weights = pd.read_csv("farm_weight_logs.csv")
    df_feeds = pd.read_csv("farm_feed_logs.csv")

    # 3. Export to PostgreSQL Tables
    print("Uploading tables to PostgreSQL...")
    df_batches.to_sql("batches", engine, if_exists="replace", index=False)
    df_weights.to_sql("weight_logs", engine, if_exists="replace", index=False)
    df_feeds.to_sql("feed_logs", engine, if_exists="replace", index=False)

    print("✅ Success! Tables ['batches', 'weight_logs', 'feed_logs'] are now live in PostgreSQL.")

except Exception as e:
    print(f"❌ Connection Failed: {e}")