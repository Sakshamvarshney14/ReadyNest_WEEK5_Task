import os
import pandas as pd

# ==========================================================
# PATHS
# ==========================================================

RAW_DATA_PATH = "data/raw/ecommerce_full_data.csv"
CLEANED_DATA_PATH = "data/cleaned/cleaned_data.csv"
REPORT_PATH = "reports/data_cleaning_report.txt"

os.makedirs("data/cleaned", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(RAW_DATA_PATH)

original_shape = df.shape

report = []
report.append("=" * 70)
report.append("DATA CLEANING REPORT")
report.append("=" * 70)
report.append(f"Original Shape : {original_shape}")

# ==========================================================
# REMOVE EXACT DUPLICATES
# ==========================================================

duplicate_rows = df.duplicated().sum()

df = df.drop_duplicates().reset_index(drop=True)

report.append(f"Exact Duplicate Rows Removed : {duplicate_rows}")

# ==========================================================
# REMOVE EXTRA SPACES
# ==========================================================

text_columns = [
    "Gender",
    "Location",
    "ProductCategory",
    "PaymentMethod",
    "ChurnStatus"
]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", pd.NA)

report.append("Leading/Trailing Spaces Removed")

# ==========================================================
# STANDARDIZE GENDER
# ==========================================================

gender_map = {
    "M": "Male",
    "Male": "Male",
    "m": "Male",
    "male": "Male",

    "F": "Female",
    "Female": "Female",
    "f": "Female",
    "female": "Female"
}

df["Gender"] = df["Gender"].replace(gender_map)

report.append("Gender Standardized")

# ==========================================================
# STANDARDIZE PRODUCT CATEGORY
# ==========================================================

category_map = {

    "Elec": "Electronics",
    "electronics": "Electronics",

    "Electronics": "Electronics",

    "Beauty": "Beauty",
    "Fashion": "Fashion",
    "Home": "Home"
}

df["ProductCategory"] = df["ProductCategory"].replace(category_map)

report.append("Product Categories Standardized")

# ==========================================================
# STANDARDIZE CHURN STATUS
# ==========================================================

churn_map = {
    "yes": "Yes",
    "Yes": "Yes",
    "no": "No",
    "No": "No"
}

df["ChurnStatus"] = df["ChurnStatus"].replace(churn_map)

report.append("Churn Status Standardized")

# ==========================================================
# CONVERT DATE
# ==========================================================

df["PurchaseDate"] = pd.to_datetime(
    df["PurchaseDate"],
    errors="coerce"
)

report.append("PurchaseDate Converted To Datetime")

# ==========================================================
# MISSING VALUE HANDLING
# ==========================================================

# Age
age_missing = df["Age"].isna().sum()
age_median = df["Age"].median()

df["Age"] = df["Age"].fillna(age_median)

report.append(
    f"Age Missing Filled : {age_missing} (Median = {age_median})"
)

# Location

location_missing = df["Location"].isna().sum()
location_mode = df["Location"].mode()[0]

df["Location"] = df["Location"].fillna(location_mode)

report.append(
    f"Location Missing Filled : {location_missing} (Mode = {location_mode})"
)

# Customer Rating

rating_missing = df["CustomerRating"].isna().sum()
rating_median = df["CustomerRating"].median()

df["CustomerRating"] = df["CustomerRating"].fillna(rating_median)

report.append(
    f"CustomerRating Missing Filled : {rating_missing} (Median = {rating_median})"
)

# Total Amount

amount_missing = df["TotalAmount"].isna().sum()

calculated_amount = (
    df["Quantity"]
    * df["UnitPrice"]
    * (1 - df["DiscountPercent"] / 100)
) + df["ShippingCost"]

df["TotalAmount"] = df["TotalAmount"].fillna(calculated_amount)

report.append(
    f"TotalAmount Missing Filled : {amount_missing} (Business Formula)"
)

# ==========================================================
# FINAL DUPLICATE REMOVAL
# ==========================================================

print("\nRemoving Final Duplicate Records...")

before_final = len(df)

df = df.drop_duplicates().reset_index(drop=True)

after_final = len(df)

final_duplicates_removed = before_final - after_final

report.append(
    f"Final Duplicate Rows Removed : {final_duplicates_removed}"
)

print(f"Final Duplicate Rows Removed : {final_duplicates_removed}")

# ==========================================================
# FINAL VALIDATION
# ==========================================================

remaining_missing = df.isnull().sum().sum()

report.append("")
report.append(f"Remaining Missing Values : {remaining_missing}")
report.append(f"Final Shape : {df.shape}")

# ==========================================================
# SAVE DATASET
# ==========================================================

df.to_csv(CLEANED_DATA_PATH, index=False)

# ==========================================================
# SAVE REPORT
# ==========================================================

with open(REPORT_PATH, "w", encoding="utf-8") as f:

    for line in report:
        f.write(str(line) + "\n")

# ==========================================================
# CONSOLE OUTPUT
# ==========================================================

print("=" * 70)
print("DATA CLEANING COMPLETED")
print("=" * 70)

print(f"Original Shape      : {original_shape}")
print(f"Final Shape         : {df.shape}")
print(f"Duplicates Removed  : {duplicate_rows}")
print(f"Final Duplicates Removed : {final_duplicates_removed}")
print(f"Remaining Missing   : {remaining_missing}")

print("\nCleaned Dataset Saved At")
print(CLEANED_DATA_PATH)

print("\nCleaning Report Saved At")
print(REPORT_PATH)

print("\nUnique Gender Values")
print(df["Gender"].unique())

print("\nUnique Product Categories")
print(df["ProductCategory"].unique())

print("\nUnique Churn Values")
print(df["ChurnStatus"].unique())