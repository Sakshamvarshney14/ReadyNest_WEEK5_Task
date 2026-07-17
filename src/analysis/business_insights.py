import os
import pandas as pd

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = "data/processed/feature_engineered_data.csv"

REPORT_PATH = "reports/business_insights_report.txt"

os.makedirs("reports", exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATA_PATH)

report = []

report.append("=" * 70)
report.append("BUSINESS INSIGHTS REPORT")
report.append("=" * 70)

print("=" * 70)
print("BUSINESS INSIGHTS")
print("=" * 70)

# ==========================================================
# KPI
# ==========================================================

total_revenue = df["TotalAmount"].sum()

total_orders = len(df)

avg_order = df["TotalAmount"].mean()

report.append(f"Total Revenue : {total_revenue:.2f}")
report.append(f"Total Orders : {total_orders}")
report.append(f"Average Order Value : {avg_order:.2f}")

# ==========================================================
# TOP PRODUCT CATEGORY
# ==========================================================

top_category = (
    df.groupby("ProductCategory")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
)

report.append("")
report.append("Top Revenue Product Category")
report.append(str(top_category.head(3)))

# ==========================================================
# TOP LOCATION
# ==========================================================

top_location = (
    df.groupby("Location")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
)

report.append("")
report.append("Top Revenue Locations")
report.append(str(top_location.head(3)))

# ==========================================================
# PAYMENT METHOD
# ==========================================================

payment = (
    df.groupby("PaymentMethod")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
)

report.append("")
report.append("Revenue By Payment Method")
report.append(str(payment))

# ==========================================================
# CHURN RATE
# ==========================================================

churn_rate = (
    df["ChurnStatus"]
    .value_counts(normalize=True)
    * 100
)

report.append("")
report.append("Customer Churn Rate (%)")
report.append(str(churn_rate.round(2)))

# ==========================================================
# HIGH VALUE CUSTOMERS
# ==========================================================

high_value = (
    df["HighValueCustomer"]
    .value_counts()
)

report.append("")
report.append("High Value Customers")
report.append(str(high_value))

# ==========================================================
# CUSTOMER SEGMENT
# ==========================================================

segments = (
    df["CustomerSegment"]
    .value_counts()
)

report.append("")
report.append("Customer Segments")
report.append(str(segments))

# ==========================================================
# WEEKEND SALES
# ==========================================================

weekend_sales = (
    df.groupby("WeekendPurchase")["TotalAmount"]
    .sum()
)

report.append("")
report.append("Weekend vs Weekday Revenue")
report.append(str(weekend_sales))

# ==========================================================
# RATING ANALYSIS
# ==========================================================

rating = (
    df.groupby("RatingCategory")["TotalAmount"]
    .mean()
)

report.append("")
report.append("Average Revenue by Rating")
report.append(str(rating.round(2)))

# ==========================================================
# DISCOUNT IMPACT
# ==========================================================

discount = (
    df.groupby("DiscountCategory")["TotalAmount"]
    .mean()
)

report.append("")
report.append("Average Revenue by Discount")
report.append(str(discount.round(2)))

# ==========================================================
# SAVE REPORT
# ==========================================================

with open(REPORT_PATH, "w", encoding="utf-8") as f:

    for line in report:
        f.write(str(line) + "\n")

print("\nBusiness Insights Generated Successfully")

print(REPORT_PATH)