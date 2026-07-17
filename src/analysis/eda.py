import os
import pandas as pd
import numpy as np

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = "data/processed/feature_engineered_data.csv"

REPORT_PATH = "reports/eda_summary_report.txt"

os.makedirs("reports", exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATA_PATH)

report = []

report.append("=" * 70)
report.append("EXPLORATORY DATA ANALYSIS REPORT")
report.append("=" * 70)

print("=" * 70)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# ==========================================================
# DATASET OVERVIEW
# ==========================================================

report.append("\nDATASET OVERVIEW")

report.append(f"Rows : {df.shape[0]}")
report.append(f"Columns : {df.shape[1]}")

print("\nDataset Shape :", df.shape)

# ==========================================================
# MISSING VALUES
# ==========================================================

missing = df.isnull().sum().sum()

report.append(f"\nMissing Values : {missing}")

print("Missing Values :", missing)

# ==========================================================
# DUPLICATES
# ==========================================================

duplicates = df.duplicated().sum()

report.append(f"Duplicate Rows : {duplicates}")

print("Duplicate Rows :", duplicates)

# ==========================================================
# NUMERICAL FEATURES
# ==========================================================

numerical = df.select_dtypes(include=np.number)

report.append("\nNUMERICAL FEATURES")

for col in numerical.columns:

    report.append(f"{col}")

# ==========================================================
# CATEGORICAL FEATURES
# ==========================================================

categorical = df.select_dtypes(exclude=np.number)

report.append("\nCATEGORICAL FEATURES")

for col in categorical.columns:

    report.append(f"{col}")

# ==========================================================
# TOP LOCATIONS
# ==========================================================

report.append("\nTOP LOCATIONS")

top_locations = df["Location"].value_counts()

for location, count in top_locations.items():

    report.append(f"{location} : {count}")

# ==========================================================
# PRODUCT CATEGORY
# ==========================================================

report.append("\nPRODUCT CATEGORIES")

category = df["ProductCategory"].value_counts()

for cat, count in category.items():

    report.append(f"{cat} : {count}")

# ==========================================================
# PAYMENT METHOD
# ==========================================================

report.append("\nPAYMENT METHODS")

payment = df["PaymentMethod"].value_counts()

for method, count in payment.items():

    report.append(f"{method} : {count}")

# ==========================================================
# CUSTOMER SEGMENT
# ==========================================================

report.append("\nCUSTOMER SEGMENTS")

segments = df["CustomerSegment"].value_counts()

for segment, count in segments.items():

    report.append(f"{segment} : {count}")

# ==========================================================
# CHURN
# ==========================================================

report.append("\nCHURN STATUS")

churn = df["ChurnStatus"].value_counts()

for status, count in churn.items():

    report.append(f"{status} : {count}")

# ==========================================================
# BUSINESS METRICS
# ==========================================================

report.append("\nBUSINESS METRICS")

report.append(f"Total Revenue : {round(df['TotalAmount'].sum(),2)}")

report.append(f"Average Order Value : {round(df['TotalAmount'].mean(),2)}")

report.append(f"Highest Order : {round(df['TotalAmount'].max(),2)}")

report.append(f"Average Rating : {round(df['CustomerRating'].mean(),2)}")

report.append(f"Average Discount : {round(df['DiscountPercent'].mean(),2)}")

# ==========================================================
# SAVE REPORT
# ==========================================================

with open(REPORT_PATH,"w",encoding="utf-8") as f:

    for line in report:

        f.write(str(line)+"\n")

print("\nEDA Summary Report Saved Successfully")

print(REPORT_PATH)

print("\nEDA Completed Successfully")