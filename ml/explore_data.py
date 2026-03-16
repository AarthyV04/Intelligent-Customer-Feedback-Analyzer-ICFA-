"""
Day 1 / Day 2 - Person 4
Explore the churn dataset before building the model.

Run: python ml/explore_data.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_PATH = "ml/sample_data/churn_data.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 50)
print("STEP 1: Raw Data Info")
print("=" * 50)
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
print("Columns:")
for col in df.columns:
    print(f"  - {col} ({df[col].dtype})")

print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# Clean
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

print("\n" + "=" * 50)
print("STEP 2: After Cleaning")
print("=" * 50)
print(f"Shape after clean: {df.shape}")
print(f"Churn = 1 (leaves): {df['Churn'].sum()}")
print(f"Churn = 0 (stays):  {(df['Churn'] == 0).sum()}")

print("\n" + "=" * 50)
print("STEP 3: Key Patterns")
print("=" * 50)
print("Avg tenure (0=stays, 1=leaves):")
print(df.groupby("Churn")["tenure"].mean())
print("\nAvg monthly charges:")
print(df.groupby("Churn")["MonthlyCharges"].mean())
print("\nChurn rate by contract type:")
print(df.groupby("Contract")["Churn"].mean().sort_values(ascending=False))

# Charts
os.makedirs("ml/charts", exist_ok=True)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

df.groupby("Contract")["Churn"].mean().plot(
    kind="bar", ax=axes[0], color=["#4CAF50", "#FF9800", "#F44336"]
)
axes[0].set_title("Churn Rate by Contract Type")
axes[0].set_ylabel("Churn Rate")

df[df["Churn"] == 1]["MonthlyCharges"].hist(ax=axes[1], color="#F44336", alpha=0.7, label="Churned")
df[df["Churn"] == 0]["MonthlyCharges"].hist(ax=axes[1], color="#4CAF50", alpha=0.7, label="Stayed")
axes[1].set_title("Monthly Charges: Churned vs Stayed")
axes[1].legend()

df[df["Churn"] == 1]["tenure"].hist(ax=axes[2], color="#F44336", alpha=0.7, label="Churned")
df[df["Churn"] == 0]["tenure"].hist(ax=axes[2], color="#4CAF50", alpha=0.7, label="Stayed")
axes[2].set_title("Tenure: Churned vs Stayed")
axes[2].legend()

plt.tight_layout()
plt.savefig("ml/charts/eda_charts.png")
print("\nCharts saved to ml/charts/eda_charts.png")
plt.show()
