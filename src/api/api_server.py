import os
import joblib
import pandas as pd
import numpy as np

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ==========================================================
# APP
# ==========================================================

app = FastAPI(
    title="Retail Analytics API",
    version="1.0"
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "feature_engineered_data.csv"
)

PREDICTION_PATH = os.path.join(
    BASE_DIR,
    "data",
    "predictions",
    "predictions.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "best_model.pkl"
)

# ==========================================================
# LOAD FILES
# ==========================================================

dataset = pd.read_csv(DATA_PATH)

predictions = pd.read_csv(PREDICTION_PATH)

model = joblib.load(MODEL_PATH)

# ==========================================================
# HEALTH
# ==========================================================

@app.get("/health")

def health():

    return {

        "status": "running",

        "dataset_loaded": True,

        "prediction_file_loaded": True,

        "model_loaded": True

    }

# ==========================================================
# SUMMARY
# ==========================================================

@app.get("/summary")

def summary():

    churn_rate = (
        (
            dataset["ChurnStatus"]
            .str.lower()
            .eq("yes")
            .mean()
        ) * 100
    )

    return {

        "total_records": int(len(dataset)),

        "total_revenue": float(dataset["TotalAmount"].sum()),

        "average_order_value": float(
            dataset["TotalAmount"].mean()
        ),

        "average_rating": float(
            dataset["CustomerRating"].mean()
        ),

        "high_value_customers": int(

            (
                dataset["HighValueCustomer"] == "Yes"

            ).sum()

        ),

        "churn_rate": round(churn_rate,2)

    }
    
# ==========================================================
# COMPLETE DATASET
# ==========================================================

@app.get("/dataset")

def get_dataset():

    return dataset.to_dict(
        orient="records"
    )

# ==========================================================
# TOP CUSTOMERS
# ==========================================================

@app.get("/top-customers")

def top_customers():

    top = (

        dataset

        .sort_values(

            "TotalAmount",

            ascending=False

        )

        .head(10)

    )

    return top.to_dict(

        orient="records"

    )

# ==========================================================
# CATEGORY REVENUE
# ==========================================================

@app.get("/category-revenue")

def category_revenue():

    revenue = (

        dataset

        .groupby(

            "ProductCategory",

            as_index=False

        )["TotalAmount"]

        .sum()

        .sort_values(

            "TotalAmount",

            ascending=False

        )

    )

    return revenue.to_dict(

        orient="records"

    )

# ==========================================================
# LOCATION REVENUE
# ==========================================================

@app.get("/location-revenue")

def location_revenue():

    revenue = (

        dataset

        .groupby(

            "Location",

            as_index=False

        )["TotalAmount"]

        .sum()

        .sort_values(

            "TotalAmount",

            ascending=False

        )

    )

    return revenue.to_dict(

        orient="records"

    )

# ==========================================================
# PAYMENT ANALYSIS
# ==========================================================

@app.get("/payment-analysis")

def payment_analysis():

    payment = (

        dataset

        .groupby(

            "PaymentMethod",

            as_index=False

        )

        .size()

        .rename(

            columns={

                "size":"Count"

            }

        )

        .sort_values(

            "Count",

            ascending=False

        )

    )

    return payment.to_dict(

        orient="records"

    )

# ==========================================================
# CUSTOMER SEGMENTS
# ==========================================================

@app.get("/customer-segments")

def customer_segments():

    segments = (

        dataset

        .groupby(

            "CustomerSegment",

            as_index=False

        )

        .size()

        .rename(

            columns={

                "size":"Count"

            }

        )

        .sort_values(

            "Count",

            ascending=False

        )

    )

    return segments.to_dict(

        orient="records"

    )
    
# ==========================================================
# PREDICTIONS
# ==========================================================

@app.get("/predictions")

def get_predictions():

    return predictions.to_dict(
        orient="records"
    )

# ==========================================================
# MODEL METRICS
# ==========================================================

@app.get("/model-metrics")

def model_metrics():

    accuracy = 0.7276

    precision = 0.7174

    recall = 0.9802

    f1_score = 0.8285

    return {

        "model": "Random Forest",

        "accuracy": accuracy,

        "precision": precision,

        "recall": recall,

        "f1_score": f1_score

    }

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

@app.get("/business-insights")

def business_insights():

    insights = []

    churn_rate = (
        dataset["ChurnStatus"]
        .str.lower()
        .eq("yes")
        .mean() * 100
    )

    avg_rating = dataset["CustomerRating"].mean()

    top_category = (

        dataset.groupby("ProductCategory")["TotalAmount"]

        .sum()

        .idxmax()

    )

    top_location = (

        dataset.groupby("Location")["TotalAmount"]

        .sum()

        .idxmax()

    )

    if churn_rate > 40:

        insights.append(
            "Customer churn is high. Focus on customer retention."
        )

    else:

        insights.append(
            "Customer churn is under control."
        )

    if avg_rating >= 4:

        insights.append(
            "Customer satisfaction is good."
        )

    else:

        insights.append(
            "Customer ratings need improvement."
        )

    insights.append(
        f"Top revenue category: {top_category}"
    )

    insights.append(
        f"Top performing location: {top_location}"
    )

    return {

        "insights": insights

    }

# ==========================================================
# API ROOT
# ==========================================================

@app.get("/")

def root():

    return {

        "message": "Retail Analytics API Running",

        "version": "1.0",

        "available_endpoints": [

            "/health",

            "/summary",

            "/dataset",

            "/predictions",

            "/top-customers",

            "/category-revenue",

            "/location-revenue",

            "/payment-analysis",

            "/customer-segments",

            "/business-insights",

            "/model-metrics"

        ]

    }

# ==========================================================
# RUN SERVER
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "api_server:app",

        host="127.0.0.1",

        port=8000,

        reload=True

    )