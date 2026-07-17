import os
import pandas as pd
import numpy as np

RAW_DATA_PATH = "data/raw/ecommerce_full_data.csv"
REPORT_PATH = "reports/data_consistency_report.txt"

os.makedirs("reports", exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(RAW_DATA_PATH)

print("=" * 70)
print("DATA CONSISTENCY CHECK")
print("=" * 70)

report = []

report.append("=" * 70)
report.append("DATA CONSISTENCY REPORT")
report.append("=" * 70)

# ==========================================================
# Calculate Expected TotalAmount
# ==========================================================

expected_total = (
    df["Quantity"]
    * df["UnitPrice"]
    * (1 - df["DiscountPercent"] / 100)
) + df["ShippingCost"]

comparison = pd.DataFrame({
    "Actual": df["TotalAmount"],
    "Expected": expected_total
})

comparison = comparison.dropna()

comparison["Difference"] = abs(
    comparison["Actual"] - comparison["Expected"]
)

tolerance = 0.01

matched = (comparison["Difference"] <= tolerance).sum()
not_matched = (comparison["Difference"] > tolerance).sum()

total_checked = len(comparison)

match_percent = (matched / total_checked) * 100

print(f"\nRows Checked : {total_checked}")
print(f"Matched      : {matched}")
print(f"Not Matched  : {not_matched}")
print(f"Match %      : {match_percent:.2f}%")

report.append(f"\nRows Checked : {total_checked}")
report.append(f"Matched : {matched}")
report.append(f"Not Matched : {not_matched}")
report.append(f"Match Percentage : {match_percent:.2f}%")

# ==========================================================
# Sample mismatches
# ==========================================================

if not_matched > 0:

    report.append("\nSample Mismatches")
    report.append("-" * 40)

    mismatch_df = comparison[comparison["Difference"] > tolerance].head(10)

    report.append(mismatch_df.to_string())

# ==========================================================
# Save Report
# ==========================================================

with open(REPORT_PATH, "w", encoding="utf-8") as f:

    for line in report:
        f.write(str(line) + "\n")

print("\nConsistency Report Saved Successfully.")
print(REPORT_PATH)