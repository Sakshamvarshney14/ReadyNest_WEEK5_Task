import requests
import pandas as pd
import streamlit as st

# ==========================================================
# API CONFIG
# ==========================================================

BASE_URL = "https://readynest-week5-task.onrender.com"

# ==========================================================
# SAFE API REQUEST
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def fetch(endpoint):

    try:

        response = requests.get(
            f"{BASE_URL}{endpoint}",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return None


# ==========================================================
# HEALTH
# ==========================================================

@st.cache_data(ttl=30, show_spinner=False)
def get_health():

    return fetch("/health")


# ==========================================================
# SUMMARY
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_summary():

    return fetch("/summary")


# ==========================================================
# DATASET
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_dataset():

    data = fetch("/dataset")

    if data is None:
        return pd.DataFrame()

    return pd.DataFrame(data)


# ==========================================================
# PREDICTIONS
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_predictions():

    data = fetch("/predictions")

    if data is None:
        return pd.DataFrame()

    return pd.DataFrame(data)


# ==========================================================
# TOP CUSTOMERS
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_top_customers():

    data = fetch("/top-customers")

    if data is None:
        return pd.DataFrame()

    return pd.DataFrame(data)


# ==========================================================
# CATEGORY REVENUE
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_category_revenue():

    data = fetch("/category-revenue")

    if data is None:
        return pd.DataFrame()

    return pd.DataFrame(data)


# ==========================================================
# LOCATION REVENUE
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_location_revenue():

    data = fetch("/location-revenue")

    if data is None:
        return pd.DataFrame()

    return pd.DataFrame(data)


# ==========================================================
# PAYMENT ANALYSIS
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_payment_analysis():

    data = fetch("/payment-analysis")

    if data is None:
        return pd.DataFrame()

    return pd.DataFrame(data)


# ==========================================================
# CUSTOMER SEGMENTS
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_customer_segments():

    data = fetch("/customer-segments")

    if data is None:
        return pd.DataFrame()

    return pd.DataFrame(data)


# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_business_insights():

    data = fetch("/business-insights")

    if data is None:
        return []

    return data.get("insights", [])


# ==========================================================
# MODEL METRICS
# ==========================================================

@st.cache_data(ttl=60, show_spinner=False)
def get_model_metrics():

    data = fetch("/model-metrics")

    if data is None:
        return {}

    return data


# ==========================================================
# API STATUS
# ==========================================================

def api_status():

    health = get_health()

    if health is None:
        return {
            "status": "offline",
            "dataset_loaded": False,
            "model_loaded": False,
            "prediction_file_loaded": False
        }

    return health


# ==========================================================
# REFRESH DASHBOARD
# ==========================================================

def refresh_dashboard():

    st.cache_data.clear()


# ==========================================================
# FORMATTERS
# ==========================================================

def currency(value):

    try:
        return f"₹{float(value):,.2f}"
    except Exception:
        return "₹0.00"


def number(value):

    try:
        return f"{int(value):,}"
    except Exception:
        return "0"


def percentage(value):

    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "0.00%"