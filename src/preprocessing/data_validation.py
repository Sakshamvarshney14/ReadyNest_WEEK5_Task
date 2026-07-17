import os
import pandas as pd

RAW_DATA_PATH = "data/raw/ecommerce_full_data.csv"
REPORT_PATH = "reports/data_validation_report.txt"

os.makedirs("reports", exist_ok=True)

df = pd.read_csv(RAW_DATA_PATH)

report = []

report.append("=" * 60)
report.append("DATA VALIDATION REPORT")
report.append("=" * 60)

print("=" * 60)
print("DATA VALIDATION")
print("=" * 60)

# ----------------------------------------------------
# Dataset Shape
# ----------------------------------------------------

report.append(f"\nShape : {df.shape}")

# ----------------------------------------------------
# Exact Duplicate Rows
# ----------------------------------------------------

duplicate_rows = df.duplicated().sum()

report.append(f"\nExact Duplicate Rows : {duplicate_rows}")

print(f"\nExact Duplicate Rows : {duplicate_rows}")

# ----------------------------------------------------
# Duplicate Transaction IDs
# ----------------------------------------------------

duplicate_ids = df["TransactionID"].duplicated().sum()

report.append(f"\nDuplicate Transaction IDs : {duplicate_ids}")

print(f"Duplicate Transaction IDs : {duplicate_ids}")

# ----------------------------------------------------
# Unique Values
# ----------------------------------------------------

categorical_columns = [
    "Gender",
    "Location",
    "ProductCategory",
    "PaymentMethod",
    "ChurnStatus"
]

for col in categorical_columns:

    values = sorted(df[col].dropna().astype(str).unique())

    report.append(f"\n{col}")
    report.append("-" * len(col))

    for v in values:
        report.append(v)

    print(f"\n{col}")
    print(values)

# ----------------------------------------------------
# Missing Values
# ----------------------------------------------------

missing = df.isnull().sum()

report.append("\nMissing Values")
report.append("-" * 30)

for col in df.columns:

    if missing[col] > 0:
        report.append(f"{col} : {missing[col]}")

# ----------------------------------------------------
# Save Report
# ----------------------------------------------------

with open(REPORT_PATH, "w", encoding="utf-8") as f:

    for line in report:
        f.write(str(line) + "\n")

print("\nValidation Report Saved Successfully.")
print(REPORT_PATH)