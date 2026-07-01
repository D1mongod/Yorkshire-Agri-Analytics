import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Загружаем секреты из .env
load_dotenv()

# 2. Теперь определяем переменную db_url, используя данные из .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME")

db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# 3. Дальше идет ваш основной код, который использует db_url
# ... например: engine = create_engine(db_url)
print("--- Fetching Data from PostgreSQL for Visualisation --- \n")

# 1. Connect to your PostgreSQL database
#db_url = "postgresql://postgres:********@localhost:5432/yorkshire_farm"
engine = create_engine(db_url)

# 2. SQL Query to get weight dynamics over 20 weeks
query = 'SELECT "Batch_ID", "Week_Number", "Avg_Weight_kg" FROM weight_logs;'
df = pd.read_sql(query, engine)

# 3. Set up the plotting style using Seaborn
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))

# 4. Create a line plot showing growth curves for all batches
# hue="Batch_ID" will automatically color-code each pig group
sns.lineplot(
   data=df, x="Week_Number", y="Avg_Weight_kg", hue="Batch_ID", linewidth=2.5
)

# 5. Customise the chart (Adding UK business context)
plt.title(
   "Yorkshire Agri-Farm: Livestock Growth Curve Analysis (20 Weeks)",
   fontsize=14,
   fontweight="bold",
   pad=15,
)
plt.xlabel("Week of Feeding Cycle", fontsize=12)
plt.ylabel("Average Weight (kg)", fontsize=12)
plt.xticks(range(1, 21))  # Show every week from 1 to 20

# Highlight the target market weight (110kg) line
plt.axhline(y=110, color="green", linestyle="--", alpha=0.7, label="Target (110kg)")

# Add a text annotation pointing to our anomaly
plt.text(
   15,
   75,
   "ALERT: Batch B03 Underperforming Growth",
   color="red",
   fontweight="bold",
)

plt.legend(title="Animal Batches")
plt.tight_layout()

# Save the final chart as an image for your GitHub README!
plt.savefig("yorkshire_farm_growth_curve.png", dpi=300)
print("✅ Success! Chart saved to your project folder as 'yorkshire_farm_growth_curve.png'")

# Display the chart on your screen
plt.show()
