import os
import pandas as pd
import numpy as np

# ==========================================================
# PATHS
# ==========================================================

CLEANED_DATA_PATH = "data/cleaned/cleaned_data.csv"
PROCESSED_DATA_PATH = "data/processed/feature_engineered_data.csv"
REPORT_PATH = "reports/feature_engineering_report.txt"

os.makedirs("data/processed", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(CLEANED_DATA_PATH)

initial_shape = df.shape
initial_columns = len(df.columns)

report = []

report.append("=" * 70)
report.append("FEATURE ENGINEERING REPORT")
report.append("=" * 70)
report.append(f"Initial Shape : {initial_shape}")

print("=" * 70)
print("FEATURE ENGINEERING")
print("=" * 70)

# ==========================================================
# DATE FEATURES
# ==========================================================

df["PurchaseDate"] = pd.to_datetime(df["PurchaseDate"])

df["PurchaseYear"] = df["PurchaseDate"].dt.year

df["PurchaseMonth"] = df["PurchaseDate"].dt.month

df["MonthName"] = df["PurchaseDate"].dt.month_name()

df["PurchaseDay"] = df["PurchaseDate"].dt.day

df["WeekOfMonth"] = (
    ((df["PurchaseDate"].dt.day - 1) // 7) + 1
)

week_map = {
    1: "Week 1",
    2: "Week 2",
    3: "Week 3",
    4: "Week 4",
    5: "Week 5"
}

df["WeekOfMonth"] = df["WeekOfMonth"].map(week_map)

df["DayOfWeek"] = df["PurchaseDate"].dt.day_name()

df["WeekendPurchase"] = np.where(
    df["PurchaseDate"].dt.weekday >= 5,
    "Yes",
    "No"
)

report.append("Created PurchaseYear")
report.append("Created PurchaseMonth")
report.append("Created MonthName")
report.append("Created PurchaseDay")
report.append("Created WeekOfMonth")
report.append("Created DayOfWeek")
report.append("Created WeekendPurchase")

# ==========================================================
# AGE GROUP
# ==========================================================

age_bins = [17, 25, 35, 50, 70]

age_labels = [
    "Young Adult",
    "Adult",
    "Middle Age",
    "Senior"
]

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=age_bins,
    labels=age_labels
)

report.append("Created AgeGroup")

# ==========================================================
# SPENDING CATEGORY
# ==========================================================

q1 = df["TotalAmount"].quantile(0.25)
q2 = df["TotalAmount"].quantile(0.50)
q3 = df["TotalAmount"].quantile(0.75)

def spending_category(x):

    if x <= q1:
        return "Low"

    elif x <= q2:
        return "Medium"

    elif x <= q3:
        return "High"

    return "Premium"


df["SpendingCategory"] = df["TotalAmount"].apply(
    spending_category
)

report.append("Created SpendingCategory")

# ==========================================================
# DISCOUNT CATEGORY
# ==========================================================

def discount_category(x):

    if x == 0:
        return "No Discount"

    elif x <= 5:
        return "Low Discount"

    elif x <= 10:
        return "Medium Discount"

    return "High Discount"


df["DiscountCategory"] = df["DiscountPercent"].apply(
    discount_category
)

report.append("Created DiscountCategory")

# ==========================================================
# CUSTOMER RATING CATEGORY
# ==========================================================

def rating_category(x):

    if x <= 2:
        return "Low"

    elif x == 3:
        return "Average"

    return "High"


df["RatingCategory"] = df["CustomerRating"].apply(
    rating_category
)

report.append("Created RatingCategory")

# ==========================================================
# NUMERICAL FEATURES
# ==========================================================

df["RevenuePerItem"] = (
    df["TotalAmount"] /
    df["Quantity"]
).round(2)

report.append("Created RevenuePerItem")

df["NetProductValue"] = (
    df["Quantity"]
    * df["UnitPrice"]
    * (1 - df["DiscountPercent"] / 100)
).round(2)

report.append("Created NetProductValue")

df["AverageSellingPrice"] = (
    df["NetProductValue"] /
    df["Quantity"]
).round(2)

report.append("Created AverageSellingPrice")

df["ShippingPercentage"] = (
    (
        df["ShippingCost"] /
        df["TotalAmount"]
    ) * 100
).round(2)

report.append("Created ShippingPercentage")

# ==========================================================
# SHIPPING CATEGORY
# ==========================================================

shipping_q1 = df["ShippingPercentage"].quantile(0.33)
shipping_q2 = df["ShippingPercentage"].quantile(0.66)

def shipping_category(x):

    if x <= shipping_q1:
        return "Low"

    elif x <= shipping_q2:
        return "Medium"

    return "High"


df["ShippingCategory"] = df["ShippingPercentage"].apply(
    shipping_category
)

report.append("Created ShippingCategory")

# ==========================================================
# HIGH VALUE CUSTOMER
# ==========================================================

threshold = df["TotalAmount"].quantile(0.75)

df["HighValueCustomer"] = np.where(
    df["TotalAmount"] >= threshold,
    "Yes",
    "No"
)

report.append("Created HighValueCustomer")

# ==========================================================
# CUSTOMER SEGMENT
# ==========================================================

def customer_segment(row):

    # Premium customer has highest priority
    if (
        row["HighValueCustomer"] == "Yes"
        and row["DiscountPercent"] <= 5
        and row["CustomerRating"] >= 4
    ):
        return "Premium"

    elif (
        row["HighValueCustomer"] == "Yes"
        and row["ChurnStatus"] == "No"
    ):
        return "Loyal"

    elif (
        row["HighValueCustomer"] == "Yes"
        and row["ChurnStatus"] == "Yes"
    ):
        return "At Risk"

    else:
        return "Regular"


df["CustomerSegment"] = df.apply(
    customer_segment,
    axis=1
)

report.append("Created CustomerSegment")

# ==========================================================
# ORDER VALUE CATEGORY (Extra Feature)
# ==========================================================

df["OrderValueCategory"] = pd.cut(
    df["TotalAmount"],
    bins=[0, 5000, 10000, 20000, np.inf],
    labels=[
        "Small Order",
        "Medium Order",
        "Large Order",
        "Bulk Order"
    ]
)

report.append("Created OrderValueCategory")

# ==========================================================
# FINAL REPORT
# ==========================================================

report.append("")
report.append(f"Final Shape : {df.shape}")
report.append(
    f"Total Features Added : {len(df.columns) - initial_columns}"
)

# ==========================================================
# SAVE DATASET
# ==========================================================

df.to_csv(
    PROCESSED_DATA_PATH,
    index=False
)

# ==========================================================
# SAVE REPORT
# ==========================================================

with open(REPORT_PATH, "w", encoding="utf-8") as f:

    for line in report:
        f.write(str(line) + "\n")

# ==========================================================
# CONSOLE OUTPUT
# ==========================================================

print("\n" + "=" * 70)
print("FEATURE ENGINEERING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"\nInitial Shape : {initial_shape}")
print(f"Final Shape   : {df.shape}")

print(
    f"New Features Added : {len(df.columns) - initial_columns}"
)

print("\nNew Features Created\n")

new_features = list(df.columns[initial_columns:])

for feature in new_features:
    print(f"✓ {feature}")

print("\nProcessed Dataset Saved At")
print(PROCESSED_DATA_PATH)

print("\nFeature Engineering Report Saved At")
print(REPORT_PATH)

print("\n" + "=" * 70)
print("Feature Engineering Finished")
print("=" * 70)