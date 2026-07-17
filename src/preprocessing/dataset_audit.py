import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
RAW_DATA_PATH = "data/raw/ecommerce_full_data.csv"
REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv(RAW_DATA_PATH)

print("=" * 60)
print("DATASET AUDIT REPORT")
print("=" * 60)

# -----------------------------
# Basic Information
# -----------------------------
print(f"\nShape : {df.shape}")
print(f"Rows  : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nColumn Names")
for col in df.columns:
    print("-", col)

print("\nData Types")
print(df.dtypes)

# -----------------------------
# Missing Values
# -----------------------------
missing = df.isnull().sum()

missing_df = pd.DataFrame({
    "Column": missing.index,
    "Missing Values": missing.values,
    "Percentage": (missing.values / len(df) * 100).round(2)
})

print("\nMissing Values")
print(missing_df)

# -----------------------------
# Duplicate Rows
# -----------------------------
duplicates = df.duplicated().sum()

print(f"\nDuplicate Rows : {duplicates}")

# -----------------------------
# Numerical Summary
# -----------------------------
print("\nNumerical Summary")
print(df.describe())

# -----------------------------
# Unique Values
# -----------------------------
print("\nUnique Values")

for col in df.columns:
    print(f"{col} : {df[col].nunique()}")

# -----------------------------
# Save Report
# -----------------------------
report_path = os.path.join(REPORT_DIR, "dataset_audit_report.txt")

with open(report_path, "w", encoding="utf-8") as f:

    f.write("DATASET AUDIT REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Shape : {df.shape}\n")
    f.write(f"Rows : {df.shape[0]}\n")
    f.write(f"Columns : {df.shape[1]}\n\n")

    f.write("Data Types\n")
    f.write(str(df.dtypes))
    f.write("\n\n")

    f.write("Missing Values\n")
    f.write(missing_df.to_string(index=False))
    f.write("\n\n")

    f.write(f"Duplicate Rows : {duplicates}\n\n")

    f.write("Numerical Summary\n")
    f.write(df.describe().to_string())

print("\nDataset Audit Report Saved Successfully.")
print(report_path)