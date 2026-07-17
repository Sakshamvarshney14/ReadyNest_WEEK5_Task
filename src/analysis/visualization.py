import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = "data/processed/feature_engineered_data.csv"

OUTPUT_DIR = "reports/figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("GENERATING VISUALIZATIONS")
print("=" * 70)

# ==========================================================
# FUNCTION
# ==========================================================

def save_bar(data, title, xlabel, ylabel, filename):

    plt.figure(figsize=(8,5))

    data.plot(kind="bar")

    plt.title(title)

    plt.xlabel(xlabel)

    plt.ylabel(ylabel)

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            filename
        ),
        dpi=300
    )

    plt.close()

# ==========================================================
# CUSTOMER AGE GROUP
# ==========================================================

save_bar(

    df["AgeGroup"].value_counts(),

    "Customer Age Group Distribution",

    "Age Group",

    "Customers",

    "age_group_distribution.png"

)

# ==========================================================
# GENDER
# ==========================================================

save_bar(

    df["Gender"].value_counts(),

    "Gender Distribution",

    "Gender",

    "Customers",

    "gender_distribution.png"

)

# ==========================================================
# PRODUCT CATEGORY
# ==========================================================

save_bar(

    df["ProductCategory"].value_counts(),

    "Product Category Distribution",

    "Category",

    "Orders",

    "product_category_distribution.png"

)

# ==========================================================
# PAYMENT METHOD
# ==========================================================

save_bar(

    df["PaymentMethod"].value_counts(),

    "Payment Method",

    "Method",

    "Orders",

    "payment_method_distribution.png"

)

# ==========================================================
# CUSTOMER SEGMENT
# ==========================================================

save_bar(

    df["CustomerSegment"].value_counts(),

    "Customer Segments",

    "Segment",

    "Customers",

    "customer_segment_distribution.png"

)

# ==========================================================
# CHURN
# ==========================================================

save_bar(

    df["ChurnStatus"].value_counts(),

    "Churn Distribution",

    "Status",

    "Customers",

    "churn_distribution.png"

)

# ==========================================================
# HIGH VALUE CUSTOMER
# ==========================================================

save_bar(

    df["HighValueCustomer"].value_counts(),

    "High Value Customers",

    "Category",

    "Customers",

    "high_value_customer_distribution.png"

)

print("\nPhase 1 Visualizations Completed Successfully")

print(OUTPUT_DIR)

# ==========================================================
# REVENUE BY PRODUCT CATEGORY
# ==========================================================

plt.figure(figsize=(8,5))

df.groupby("ProductCategory")["TotalAmount"].sum().sort_values().plot(kind="bar")

plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "revenue_by_product_category.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# REVENUE BY LOCATION
# ==========================================================

plt.figure(figsize=(8,5))

df.groupby("Location")["TotalAmount"].sum().sort_values().plot(kind="bar")

plt.title("Revenue by Location")
plt.xlabel("Location")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "revenue_by_location.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# MONTHLY SALES
# ==========================================================

plt.figure(figsize=(10,5))

monthly_sales = df.groupby("MonthName")["TotalAmount"].sum()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales = monthly_sales.reindex(
    [m for m in month_order if m in monthly_sales.index]
)

monthly_sales.plot(marker="o")

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "monthly_revenue.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# DISCOUNT DISTRIBUTION
# ==========================================================

plt.figure(figsize=(8,5))

df["DiscountCategory"].value_counts().plot(kind="bar")

plt.title("Discount Category Distribution")
plt.xlabel("Discount Category")
plt.ylabel("Orders")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "discount_distribution.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# ORDER VALUE CATEGORY
# ==========================================================

plt.figure(figsize=(8,5))

df["OrderValueCategory"].value_counts().plot(kind="bar")

plt.title("Order Value Category")
plt.xlabel("Category")
plt.ylabel("Orders")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "order_value_category.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# SHIPPING CATEGORY
# ==========================================================

plt.figure(figsize=(8,5))

df["ShippingCategory"].value_counts().plot(kind="bar")

plt.title("Shipping Category")
plt.xlabel("Shipping")
plt.ylabel("Orders")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "shipping_category.png"
    ),
    dpi=300
)

plt.close()

print("\nPhase 2 Visualizations Completed Successfully")

# ==========================================================
# CUSTOMER RATING DISTRIBUTION
# ==========================================================

plt.figure(figsize=(8,5))

df["CustomerRating"].value_counts().sort_index().plot(kind="bar")

plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "customer_rating_distribution.png"),
    dpi=300
)

plt.close()

# ==========================================================
# REVENUE BY PAYMENT METHOD
# ==========================================================

plt.figure(figsize=(8,5))

df.groupby("PaymentMethod")["TotalAmount"].sum().sort_values().plot(kind="bar")

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "revenue_by_payment_method.png"),
    dpi=300
)

plt.close()

# ==========================================================
# WEEKEND VS WEEKDAY SALES
# ==========================================================

plt.figure(figsize=(6,5))

df.groupby("WeekendPurchase")["TotalAmount"].sum().plot(kind="bar")

plt.title("Weekend vs Weekday Revenue")
plt.xlabel("Weekend Purchase")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "weekend_vs_weekday_revenue.png"),
    dpi=300
)

plt.close()

# ==========================================================
# CHURN BY PRODUCT CATEGORY
# ==========================================================

plt.figure(figsize=(8,5))

pd.crosstab(
    df["ProductCategory"],
    df["ChurnStatus"]
).plot(kind="bar")

plt.title("Churn by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "churn_by_product_category.png"),
    dpi=300
)

plt.close('all')

# ==========================================================
# TOP 10 CUSTOMERS BY REVENUE
# ==========================================================

plt.figure(figsize=(10,5))

top_customer = (
    df.groupby("CustomerID")["TotalAmount"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

top_customer.plot(kind="bar")

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Customer ID")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "top10_customers.png"),
    dpi=300
)

plt.close()

# ==========================================================
# TOP LOCATIONS BY REVENUE
# ==========================================================

plt.figure(figsize=(8,5))

top_locations = (
    df.groupby("Location")["TotalAmount"]
      .sum()
      .sort_values(ascending=False)
)

top_locations.plot(kind="bar")

plt.title("Top Locations by Revenue")
plt.xlabel("Location")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "top_locations_revenue.png"),
    dpi=300
)

plt.close()

print("\nPhase 3 Visualizations Completed Successfully")

# ==========================================================
# IMPORT SEABORN
# ==========================================================

import seaborn as sns

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

plt.figure(figsize=(10,8))

numeric_df = df.select_dtypes(include=["int64","float64"])

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "correlation_heatmap.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# AGE DISTRIBUTION
# ==========================================================

plt.figure(figsize=(8,5))

plt.hist(
    df["Age"],
    bins=10
)

plt.title("Age Distribution")

plt.xlabel("Age")

plt.ylabel("Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "age_distribution.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# TOTAL AMOUNT DISTRIBUTION
# ==========================================================

plt.figure(figsize=(8,5))

plt.hist(
    df["TotalAmount"],
    bins=20
)

plt.title("Revenue Distribution")

plt.xlabel("Total Amount")

plt.ylabel("Orders")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "revenue_distribution.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# SHIPPING COST DISTRIBUTION
# ==========================================================

plt.figure(figsize=(8,5))

plt.hist(
    df["ShippingCost"],
    bins=20
)

plt.title("Shipping Cost Distribution")

plt.xlabel("Shipping Cost")

plt.ylabel("Orders")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "shipping_cost_distribution.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# QUANTITY DISTRIBUTION
# ==========================================================

plt.figure(figsize=(8,5))

df["Quantity"].value_counts().sort_index().plot(kind="bar")

plt.title("Quantity Distribution")

plt.xlabel("Quantity")

plt.ylabel("Orders")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "quantity_distribution.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# BOXPLOT - TOTAL AMOUNT
# ==========================================================

plt.figure(figsize=(8,5))

plt.boxplot(df["TotalAmount"])

plt.title("Revenue Outlier Detection")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "revenue_boxplot.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# SCATTER : QUANTITY VS TOTAL AMOUNT
# ==========================================================

plt.figure(figsize=(8,5))

plt.scatter(
    df["Quantity"],
    df["TotalAmount"],
    alpha=0.6
)

plt.title("Quantity vs Revenue")

plt.xlabel("Quantity")

plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "quantity_vs_revenue.png"
    ),
    dpi=300
)

plt.close()

print("\nPhase 4 Visualizations Completed Successfully")