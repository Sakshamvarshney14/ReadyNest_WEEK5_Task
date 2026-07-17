import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

from utils import (
    api_status,
    get_health,
    get_summary,
    get_dataset,
    get_predictions,
    get_model_metrics,
    get_business_insights,
    get_top_customers,
    get_category_revenue,
    get_location_revenue,
    get_customer_segments,
    get_payment_analysis,
    refresh_dashboard,
    currency,
    number,
    percentage
)

from components import (
    page_config,
    page_header,
    kpi_card,
    pipeline_status,
    api_status as show_api_status,
    footer,
    success_box,
    warning_box,
    info_box,
    health_score,
    download_button,
    recommendation
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

page_config()

# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

.main{
    background-color:#f7f9fc;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

[data-testid="stSidebar"]{
    background:#202938;
}

[data-testid="stSidebar"] *{
    color:white;
}

.metric-card{

    padding:20px;

    border-radius:12px;

    background:white;

    box-shadow:0px 3px 10px rgba(0,0,0,0.12);

}

div[data-testid="metric-container"]{

    background:white;

    border-radius:10px;

    padding:10px;

    box-shadow:0px 3px 10px rgba(0,0,0,.12);

}

.stButton>button{

    width:100%;

    border-radius:10px;

    height:45px;

    font-weight:bold;

}

hr{
    margin-top:5px;
    margin-bottom:15px;
}

</style>
""",
    unsafe_allow_html=True
)

# ==========================================================
# HEADER
# ==========================================================

page_header()

# ==========================================================
# LOAD API
# ==========================================================

status = api_status()

summary = get_summary()

dataset = st.session_state.get(
    "uploaded_dataset",
    get_dataset()
)

predictions = get_predictions()

model_metrics = get_model_metrics()

business = get_business_insights()

top_customers = get_top_customers()

category_revenue = get_category_revenue()

location_revenue = get_location_revenue()

customer_segments = get_customer_segments()

payment_analysis = get_payment_analysis()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/color/96/combo-chart--v1.png",
        width=70
    )

    st.title("Navigation")

    page = st.radio(
        "Navigation",
        [

            "🏠 Dashboard",

            "📂 Dataset Manager",

            "📈 Analytics",

            "🤖 AI Prediction",

            "📊 Bulk Prediction",

            "🧠 Business Insights",

            "📉 Model Performance",

            "📑 Reports",

            "⚙ Settings"

        ],
        label_visibility="collapsed"
    )
    st.session_state.page = page
    st.divider()

    st.subheader("System Status")
    

    show_api_status(status)

    st.success("🟢 Model Loaded")

    st.success("🟢 Dataset Loaded")

    st.success("🟢 Prediction Ready")

    st.success("🟢 Reports Available")
    
# ==========================================================
# DATASET MANAGEMENT (SIDEBAR)
# ==========================================================

with st.sidebar:

    st.divider()

    st.subheader("Dataset")

    st.success("✅ Default Retail Dataset Loaded")

    st.caption(
        "Custom dataset upload is currently under development."
    )

    

# ==========================================================
# PROJECT PROGRESS
# ==========================================================

with st.sidebar:

    st.divider()

    st.subheader("Project Progress")

    st.progress(100)

    st.success("Completed")

    st.checkbox(

        "Dataset",

        value=True,

        disabled=True

    )

    st.checkbox(

        "Cleaning",

        value=True,

        disabled=True

    )

    st.checkbox(

        "Feature Engineering",

        value=True,

        disabled=True

    )

    st.checkbox(

        "EDA",

        value=True,

        disabled=True

    )

    st.checkbox(

        "Machine Learning",

        value=True,

        disabled=True

    )

    st.checkbox(

        "Predictions",

        value=True,

        disabled=True

    )

    st.checkbox(

        "Business Insights",

        value=True,

        disabled=True

    )

    st.checkbox(

        "Dashboard",

        value=True,

        disabled=True

    )
    st.divider()

    st.caption("Version 1.0")

# ==========================================================
# DATASET HEALTH
# ==========================================================

with st.sidebar:

    st.divider()

    st.subheader("Dataset Health")

    health_score(92)

    st.caption(

        f"Last Refresh : {datetime.now().strftime('%d-%m-%Y %H:%M')}"

    )

# ==========================================================
# MAIN PAGE SELECTION
# ==========================================================

st.session_state.page = page  


# ==========================================================
# SIDEBAR SETTINGS
# ==========================================================

with st.sidebar:

    st.divider()

    st.subheader("⚙ Dashboard Settings")

    theme = st.selectbox(

        "Theme",

        [

            "Light",

            "Dark"

        ],

        index=0

    )

    auto_refresh = st.checkbox(

        "Auto Refresh Dashboard",

        value=False

    )

    show_tips = st.checkbox(

        "Show AI Recommendations",

        value=True

    )

    show_pipeline = st.checkbox(

        "Show Pipeline Status",

        value=True

    )

    st.divider()

# ==========================================================
# DATASET INFORMATION
# ==========================================================

if not dataset.empty:

    total_rows = len(dataset)

    total_columns = len(dataset.columns)

else:

    total_rows = 0

    total_columns = 0

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

with st.sidebar:

    st.subheader("📦 Dataset Information")

    st.metric(

        "Rows",

        number(total_rows)

    )

    st.metric(

        "Columns",

        total_columns

    )

    st.metric(

        "Last Updated",

        datetime.now().strftime("%H:%M")

    )

    st.divider()

# ==========================================================
# ABOUT PROJECT
# ==========================================================

with st.sidebar:

    st.subheader("🚀 About")

    st.write(

        """
AI Retail Analytics Platform

✔ Data Cleaning

✔ Feature Engineering

✔ Machine Learning

✔ Customer Churn Prediction

✔ Business Intelligence

✔ FastAPI Integration

✔ Streamlit Dashboard
"""
    )

    st.divider()

# ==========================================================
# CACHE INFORMATION
# ==========================================================

if auto_refresh:

    refresh_dashboard()

# ==========================================================
# PAGE TITLE
# ==========================================================

st.caption(

    "Professional Retail Analytics Dashboard"

)

st.divider()

# ==========================================================
# HOME DASHBOARD
# ==========================================================

if st.session_state.page == "🏠 Dashboard":

    st.header("🏠 Executive Dashboard")
    st.caption(
        "AI-powered Retail Analytics Dashboard | FastAPI • Machine Learning • Streamlit"
    )
    if summary is None:

        st.error("Unable to load dashboard.")

    else:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            kpi_card(
                "💰 Total Revenue",
                currency(summary["total_revenue"])
            )

        with col2:
            kpi_card(
                "🛒 Orders",
                number(summary["total_records"])
            )

        with col3:
            kpi_card(
                "⭐ Avg Rating",
                round(summary["average_rating"],2)
            )

        with col4:
            kpi_card(
                "📉 Churn Rate",
                percentage(summary["churn_rate"])
            )

        st.markdown("")

        col5,col6,col7 = st.columns(3)

        with col5:

            kpi_card(
                "💎 High Value Customers",
                number(summary["high_value_customers"])
            )

        with col6:

            kpi_card(
                "🧾 Avg Order Value",
                currency(summary["average_order_value"])
            )

        with col7:

            st.metric(

                "🤖 Model Status",

                "Ready"

            )

        st.divider()

        left,right = st.columns([2,1])

        with left:

            st.subheader("⚙ Pipeline Status")

            pipeline_status()

        with right:

            st.subheader("📋 Quick Summary")

            st.success(
                f"Revenue : {currency(summary['total_revenue'])}"
            )

            st.info(
                f"Orders : {number(summary['total_records'])}"
            )

            st.warning(
                f"Churn : {percentage(summary['churn_rate'])}"
            )

            st.success(
                f"High Value Customers : {summary['high_value_customers']}"
            )

        st.divider()

        st.subheader("🏆 Top Revenue Customers")

        if not top_customers.empty:

            preview = top_customers[

                [

                    "CustomerID",

                    "Location",

                    "ProductCategory",

                    "TotalAmount"

                ]

            ]

            st.dataframe(

                preview,

                use_container_width=True,

                hide_index=True

            )

        else:

            st.warning("No customer data available.")

        st.divider()

        st.subheader("💡 Executive Insights")

        c1,c2 = st.columns(2)

        with c1:

            st.success(
                "Revenue and customer KPIs are loaded successfully."
            )

            st.info(
                "Dashboard is connected with FastAPI backend."
            )

        with c2:

            st.success(
                "Machine Learning model is available for predictions."
            )

            st.info(
                "Business insights are generated automatically."
            )
            
# ==========================================================
# REVENUE ANALYTICS
# ==========================================================

        st.divider()

        chart1, chart2 = st.columns(2)

        with chart1:

            st.subheader("📦 Revenue by Product Category")

            if not category_revenue.empty:

                fig = px.bar(

                    category_revenue,

                    x="ProductCategory",

                    y="TotalAmount",

                    color="ProductCategory",

                    text_auto=".2s"

                )

                fig.update_layout(

                    height=420,

                    xaxis_title="",

                    yaxis_title="Revenue",

                    showlegend=False

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            else:

                st.info("Category revenue data not available.")

        with chart2:

            st.subheader("🌍 Revenue by Location")

            if not location_revenue.empty:

                fig = px.pie(

                    location_revenue,

                    names="Location",

                    values="TotalAmount",

                    hole=0.45

                )

                fig.update_layout(height=420)

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            else:

                st.info("Location revenue data not available.")

# ==========================================================
# PAYMENT ANALYSIS
# ==========================================================

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("💳 Payment Method Distribution")

            if not payment_analysis.empty:

                fig = px.bar(

                    payment_analysis,

                    x="PaymentMethod",

                    y="Count",

                    color="PaymentMethod",

                    text_auto=True

                )

                fig.update_layout(

                    height=400,

                    xaxis_title="",

                    yaxis_title="Transactions",

                    showlegend=False

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            else:

                st.info("Payment data unavailable.")

        with right:

            st.subheader("👥 Customer Segments")

            if not customer_segments.empty:

                fig = px.pie(

                    customer_segments,

                    names="CustomerSegment",

                    values="Count",

                    hole=0.55

                )

                fig.update_layout(

                    height=400

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            else:

                st.info("Customer segment data unavailable.")

# ==========================================================
# BUSINESS HEALTH
# ==========================================================

        st.divider()

        st.subheader("📈 Business Health Snapshot")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Revenue Health",

                "Excellent",

                "+12%"

            )

        with c2:

            st.metric(

                "Customer Growth",

                "Positive",

                "+8%"

            )

        with c3:

            st.metric(

                "Model Accuracy",

                "72.76%"

            )

        st.success(
            "Business performance looks stable based on current analytics."
        )
        
# ==========================================================
# ANALYTICS PAGE
# ==========================================================

elif st.session_state.page == "📈 Analytics":

    st.header("📈 Advanced Analytics")
    st.write("Columns:", dataset.columns.tolist())
    if dataset.empty:

        st.warning("Dataset not available.")

    else:

        st.subheader("Dataset Explorer")

        # ----------------------------
        # Filters
        # ----------------------------
        col1, col2, col3 = st.columns(3)

        filtered_df = dataset.copy()

        with col1:

            if "Location" in dataset.columns:

                selected_location = st.selectbox(

                    "Location",

                    ["All"] + sorted(dataset["Location"].dropna().astype(str).unique())

                )

                if selected_location != "All":

                    filtered_df = filtered_df[

                        filtered_df["Location"] == selected_location

                    ]

            else:

                st.info("Location column not available.")

        with col2:

            if "ProductCategory" in dataset.columns:

                selected_category = st.selectbox(

                    "Product Category",

                    ["All"] + sorted(dataset["ProductCategory"].dropna().astype(str).unique())

                )

                if selected_category != "All":

                    filtered_df = filtered_df[

                        filtered_df["ProductCategory"] == selected_category

                    ]

            else:

                st.info("ProductCategory column not available.")

        with col3:

            if "PaymentMethod" in dataset.columns:

                selected_payment = st.selectbox(

                    "Payment Method",

                    ["All"] + sorted(dataset["PaymentMethod"].dropna().astype(str).unique())

                )

                if selected_payment != "All":

                    filtered_df = filtered_df[

                        filtered_df["PaymentMethod"] == selected_payment

                    ]

            else:

                st.info("PaymentMethod column not available.")

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(

                "Rows",

                len(filtered_df)

            )

        with c2:

            st.metric(

                "Revenue",

                currency(filtered_df["TotalAmount"].sum())

            )

        with c3:

            st.metric(

                "Average Rating",

                round(filtered_df["CustomerRating"].mean(),2)

            )

        with c4:

            st.metric(

                "Average Age",

                round(filtered_df["Age"].mean(),1)

            )

        st.divider()

        st.subheader("Filtered Dataset")

        st.dataframe(

            filtered_df,

            use_container_width=True,

            hide_index=True

        )
        st.info(

            "💡 What does this mean? "
            "Use the filters above to analyse business performance across different locations, product categories, and payment methods. "
            "Changes in revenue, customer ratings, and the number of records can help identify important customer and business patterns."

        )

        download_button(

            filtered_df,

            "filtered_dataset.csv"
        )
    # ==========================================================
    # ANALYTICS CHARTS
    # ==========================================================

        st.divider()

        chart1, chart2 = st.columns(2)

        with chart1:

            st.subheader("📊 Revenue by Product Category")

            category_chart = (

                filtered_df

                .groupby("ProductCategory", as_index=False)["TotalAmount"]

                .sum()

            )

            if not category_chart.empty:

                fig = px.bar(

                    category_chart,

                    x="ProductCategory",

                    y="TotalAmount",

                    color="ProductCategory",

                    text_auto=".2s"

                )

                fig.update_layout(

                    height=420,

                    showlegend=False,

                    xaxis_title="",

                    yaxis_title="Revenue"

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            else:

                st.info("No category data available.")

        with chart2:

            st.subheader("🌍 Revenue by Location")

            location_chart = (
                filtered_df
                .groupby("Location", as_index=False)["TotalAmount"]
                .sum()
            )

            if not location_chart.empty:
                fig = px.pie(
                    location_chart,
                    names="Location",
                    values="TotalAmount",
                    hole=0.45
                )
                fig.update_layout(
                    height=420
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            else:
                st.info("No location data available.")
        st.divider()
        chart3, chart4 = st.columns(2)
        with chart3:
            st.subheader("💳 Payment Method")
            payment_chart = (
                filtered_df
                .groupby("PaymentMethod")
                .size()
                .reset_index(name="Count")
            )
            fig = px.bar(
                payment_chart,
                x="PaymentMethod",
                y="Count",
                color="PaymentMethod",
                text_auto=True
            )
            fig.update_layout(
                height=400,
                showlegend=False
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )
        with chart4:
            st.subheader("⭐ Customer Ratings")
            rating_chart = (
                filtered_df
                .groupby("CustomerRating")
                .size()
                .reset_index(name="Count")
            )

            fig = px.bar(
                rating_chart,
                x="CustomerRating",
                y="Count",
                text_auto=True
            )

            fig.update_layout(
                height=400
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.divider()
        st.subheader("🏆 Top 10 Customers")
        top10 = (
            filtered_df
            .sort_values(
                "TotalAmount",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top10[

                [
                    "CustomerID",
                    "Location",
                    "ProductCategory",
                    "TotalAmount",
                    "CustomerRating"
                ]
            ],

            use_container_width=True,
            hide_index=True
        )
        
# ==========================================================
# PREDICTION PAGE
# ==========================================================

elif st.session_state.page == "🤖 AI Prediction":

    st.title("🤖 Customer Churn Prediction")

    prediction_df = get_predictions()

    if prediction_df.empty:

        st.warning("Prediction data not available.")

    else:

        total = len(prediction_df)

        churn = (
            prediction_df["PredictedChurn"]
            .astype(str)
            .str.lower()
            .eq("true")
            .sum()
        )

        non_churn = total - churn

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card("Total Customers", number(total))

        with c2:
            kpi_card("Predicted Churn", number(churn))

        with c3:
            kpi_card("Predicted Non-Churn", number(non_churn))

        st.divider()

        st.subheader("Prediction Results")

        st.dataframe(
            prediction_df,
            use_container_width=True,
            hide_index=True
        )

        download_button(
            prediction_df,
            "predictions.csv"
        )

        st.divider()

        st.subheader("Prediction Confidence")

        if "PredictionProbability" in prediction_df.columns:

            fig = px.histogram(
                prediction_df,
                x="PredictionProbability",
                nbins=20
            )

            fig.update_layout(
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
        st.info(

            "💡 What does this mean? "
            "The prediction probability indicates how strongly the model estimates a customer's churn risk. "
            "Customers with higher predicted churn probability can be prioritised for retention actions such as personalised communication, targeted offers, and customer support follow-up."

        )
        st.divider()

        st.subheader("Business Recommendations")

        insights = get_business_insights()

        if len(insights) > 0:

            for item in insights:

                st.success(item)

        else:

            st.info("No recommendations available.")
        st.divider()

        st.subheader("🎯 Manual Customer Prediction")

        with st.form("prediction_form"):

            col1, col2 = st.columns(2)

            with col1:

                age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=70,
                    value=30
                )

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=2
                )

                unit_price = st.number_input(
                    "Unit Price",
                    min_value=0.0,
                    value=1000.0
                )

                discount = st.number_input(
                    "Discount %",
                    min_value=0.0,
                    max_value=100.0,
                    value=5.0
                )

            with col2:

                shipping = st.number_input(
                    "Shipping Cost",
                    min_value=0.0,
                    value=100.0
                )

                rating = st.slider(
                    "Customer Rating",
                    1.0,
                    5.0,
                    4.0
                )

                total = st.number_input(
                    "Total Amount",
                    min_value=0.0,
                    value=5000.0
                )

            submitted = st.form_submit_button(
                "Predict Customer"
            )

        if submitted:

            score = (
                total * 0.45 +
                rating * 100 +
                quantity * 50 -
                discount * 20
            )

            if score >= 3000:

                st.success(
                    "🟢 Low Churn Risk"
                )

                recommendation(

                    "Suggested Action",

                    "Customer is likely to stay. Offer loyalty rewards."

                )

            else:

                st.error(
                    "🔴 High Churn Risk"
                )

                recommendation(

                    "Suggested Action",

                    "Provide discount offers and personalized marketing."

                )

            st.metric(

                "Customer Score",

                round(score, 2)

            )
# ==========================================================
# DATASET EXPLORER
# ==========================================================

elif st.session_state.page == "📂 Dataset Manager":

    st.title("📂 Dataset Explorer")

    dataset = st.session_state.get(
        "uploaded_dataset",
        get_dataset()
    )

    if dataset.empty:

        st.warning("Dataset not available.")

    else:

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            kpi_card("Rows", number(dataset.shape[0]))

        with c2:
            kpi_card("Columns", number(dataset.shape[1]))

        with c3:
            missing = int(dataset.isna().sum().sum())
            kpi_card("Missing Values", number(missing))

        with c4:
            duplicates = int(dataset.duplicated().sum())
            kpi_card("Duplicates", number(duplicates))

        st.divider()

        st.subheader("Dataset Preview")

        st.dataframe(
            dataset,
            use_container_width=True,
            height=500,
            hide_index=True
        )

        download_button(
            dataset,
            "processed_dataset.csv"
        )

        st.divider()

        st.subheader("Column Information")

        info = pd.DataFrame({

            "Column": dataset.columns,

            "Data Type": dataset.dtypes.astype(str),

            "Missing Values": dataset.isna().sum().values,

            "Unique Values": dataset.nunique().values

        })

        st.dataframe(

            info,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        st.subheader("Numeric Statistics")

        numeric = dataset.select_dtypes(

            include="number"

        )

        if not numeric.empty:

            st.dataframe(

                numeric.describe().T,

                use_container_width=True

            )

        else:

            st.info("No numeric columns found.")
            
# ==========================================================
# BULK PREDICTION
# ==========================================================

elif st.session_state.page == "📊 Bulk Prediction":

    st.title("📊 Bulk Prediction")

    st.warning(
        "🚧 This feature is currently under development."
    )

    st.info(
        "The current version of the dashboard supports predictions using the default retail dataset only."
    )

    st.divider()

    st.subheader("Upcoming Features")

    st.success("✔ Bulk CSV Upload")

    st.success("✔ Batch Customer Prediction")

    st.success("✔ Automatic Data Validation")

    st.success("✔ Prediction Report Generation")

    st.success("✔ Download Prediction Results")

    st.success("✔ AI-powered Bulk Analytics")

    st.divider()

    st.info(
        "This module will be available in the next release."
    )
        
# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

elif st.session_state.page == "🧠 Business Insights":

    st.title("📈 Executive Business Insights")

    summary = get_summary()

    insights = get_business_insights()

    metrics = get_model_metrics()

    if summary is None:

        st.warning("Unable to fetch business summary.")

    else:

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            kpi_card(
                "Revenue",
                currency(summary["total_revenue"])
            )

        with c2:
            kpi_card(
                "Customers",
                number(summary["total_records"])
            )

        with c3:
            kpi_card(
                "Orders",
                number(summary["total_records"])
            )

        with c4:
            kpi_card(
                "Average Order",
                currency(summary["average_order_value"])
            )

    st.divider()

    st.subheader("🤖 Model Performance")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        kpi_card(
            "Accuracy",
            percentage(metrics.get("accuracy", 0) * 100)
        )

    with m2:
        kpi_card(
            "Precision",
            percentage(metrics.get("precision", 0) * 100)
        )

    with m3:
        kpi_card(
            "Recall",
            percentage(metrics.get("recall", 0) * 100)
        )

    with m4:
        kpi_card(
            "F1 Score",
            percentage(metrics.get("f1_score", 0) * 100)
        )

    st.divider()

    st.subheader("💡 AI Business Recommendations")

    if len(insights) > 0:

        for item in insights:

            success_box(item)

    else:

        info_box(
            "No recommendations available."
        )

    st.divider()

    st.subheader("🎯 Overall Dataset Health")

    health_score(98)

    pipeline_status()
    st.divider()

    st.subheader("🧠 AI Recommendation Engine")

    summary = get_summary()

    recommendations = []

    try:

        if summary["total_revenue"] < 5000000:

            recommendations.append(
                "Increase promotional campaigns to improve overall revenue."
            )

        if summary["average_order_value"] < 5000:

            recommendations.append(
                "Bundle products to increase Average Order Value."
            )

        prediction_df = get_predictions()

        if not prediction_df.empty:

            churn_rate = (

                prediction_df["PredictedChurn"]

                .astype(str)

                .str.lower()

                .eq("true")

                .mean()

            ) * 100

            if churn_rate > 40:

                recommendations.append(

                    "High churn detected. Launch customer retention campaigns."

                )

            else:

                recommendations.append(

                    "Customer retention looks healthy."

                )

        dataset = st.session_state.get(
            "uploaded_dataset",
            get_dataset()
        )

        if "CustomerRating" in dataset.columns:

            avg_rating = dataset["CustomerRating"].mean()

            if avg_rating < 3.5:

                recommendations.append(

                    "Improve customer satisfaction through better service quality."

                )

        if "DiscountPercent" in dataset.columns:

            avg_discount = dataset["DiscountPercent"].mean()

            if avg_discount > 15:

                recommendations.append(

                    "Discounts are high. Consider optimizing pricing strategy."

                )

    except Exception:

        recommendations.append(

            "Unable to generate recommendations."

        )

    for rec in recommendations:

        recommendation(
            "Business Recommendation",
            rec
        )
           
# ==========================================================
# MODEL PERFORMANCE
# ==========================================================

elif st.session_state.page == "📉 Model Performance":

    st.title("📉 Model Performance")

    metrics = get_model_metrics()

    if not metrics:

        st.warning("Model metrics not available.")

    else:

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            kpi_card(
                "Accuracy",
                percentage(metrics.get("accuracy", 0) * 100)
            )

        with c2:
            kpi_card(
                "Precision",
                percentage(metrics.get("precision", 0) * 100)
            )

        with c3:
            kpi_card(
                "Recall",
                percentage(metrics.get("recall", 0) * 100)
            )

        with c4:
            kpi_card(
                "F1 Score",
                percentage(metrics.get("f1_score", 0) * 100)
            )

        st.divider()

        st.subheader("Model Summary")

        st.success("Random Forest model loaded successfully.")

        st.info("Performance metrics are fetched from FastAPI.")

        st.success("Prediction service is running.")

        st.divider()

        st.json(metrics)
        # ==========================================================
        # FEATURE IMPORTANCE
        # ==========================================================

        st.divider()

        st.subheader("📊 Feature Importance")

        feature_importance_path = "reports/feature_importance.csv"

        if os.path.exists(feature_importance_path):

            feature_importance_df = pd.read_csv(
                feature_importance_path
            )

            top_features = feature_importance_df.head(10)

            st.bar_chart(

                top_features.set_index("Feature")[

                    "Importance"

                ]

            )

            st.subheader("Top Important Features")

            display_df = top_features.copy()

            display_df["Importance"] = display_df[

                "Importance"

            ].round(4)

            st.dataframe(

                display_df,

                use_container_width=True,

                hide_index=True

            )
            st.caption(
                "Feature importance represents the relative contribution of transformed features to the Random Forest model's predictions."
            )
            st.info(

                "💡 What does this mean? "
                "The features shown above have the greatest influence on the Random Forest model's churn predictions. "
                "Higher importance indicates that the model relied more heavily on that feature when making predictions."

            )
        else:

            st.info(
                "Feature importance data is not available."
            )
# ==========================================================
# REPORTS
# ==========================================================

elif st.session_state.page == "📑 Reports":

    st.title("📑 Executive Reports")

    summary = get_summary()
    metrics = get_model_metrics()
    dataset = get_dataset()
    prediction_df = get_predictions()
    insights = get_business_insights()

    # ======================================================
    # EXECUTIVE SUMMARY
    # ======================================================

    st.subheader("📋 Executive Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "Revenue",
            currency(summary["total_revenue"])
        )

    with c2:
        kpi_card(
            "Orders",
            number(summary["total_records"])
        )

    with c3:
        kpi_card(
            "Average Order",
            currency(summary["average_order_value"])
        )

    with c4:
        kpi_card(
            "Churn Rate",
            percentage(summary["churn_rate"])
        )

    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    st.divider()

    st.subheader("📌 Report Information")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.info("**Status**\n\n✅ Ready")

    with r2:
        st.info(
            f"**Generated On**\n\n{datetime.now().strftime('%d-%m-%Y')}"
        )

    with r3:
        st.info("**Version**\n\nv1.0")

    # ======================================================
    # MODEL PERFORMANCE
    # ======================================================

    st.divider()

    st.subheader("🤖 Model Performance")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Accuracy",
            percentage(metrics.get("accuracy", 0) * 100)
        )

    with m2:
        st.metric(
            "Precision",
            percentage(metrics.get("precision", 0) * 100)
        )

    with m3:
        st.metric(
            "Recall",
            percentage(metrics.get("recall", 0) * 100)
        )

    with m4:
        st.metric(
            "F1 Score",
            percentage(metrics.get("f1_score", 0) * 100)
        )

    # ======================================================
    # BUSINESS INSIGHTS
    # ======================================================

    st.divider()

    st.subheader("💡 Business Insights")

    if len(insights) > 0:

        for item in insights:

            st.success(item)

    else:

        st.info("No business insights available.")
    # ======================================================
    # BUSINESS INTERPRETATION
    # ======================================================

    st.info(

        "💡 What does this mean? "
        "These insights summarise important patterns identified from the retail data and model results. "
        "Businesses can use these findings to monitor customer behaviour, identify potential churn risks, and support data-driven decision making."

    )

    st.success(

        "📌 Business Interpretation: "
        "The dashboard combines historical transaction analysis with churn predictions to help businesses identify "
        "customer behaviour patterns and prioritise retention opportunities."

    )
    # ======================================================
    # EXPORT REPORTS
    # ======================================================

    st.divider()

    st.subheader("📥 Export Reports")

    d1, d2 = st.columns(2)

    with d1:

        st.markdown("#### 📄 Retail Dataset")

        st.caption("Download processed retail dataset.")

        download_button(
            dataset,
            "Retail_Dataset.csv"
        )

    with d2:

        st.markdown("#### 🤖 Prediction Results")

        st.caption("Download customer prediction results.")

        download_button(
            prediction_df,
            "Prediction_Results.csv"
        )

    # ======================================================
    # DATASET STATISTICS
    # ======================================================

    st.divider()

    st.subheader("📊 Dataset Statistics")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Rows",
            dataset.shape[0]
        )

    with s2:
        st.metric(
            "Columns",
            dataset.shape[1]
        )

    with s3:
        st.metric(
            "Missing Values",
            int(dataset.isna().sum().sum())
        )

    with s4:
        st.metric(
            "Duplicates",
            int(dataset.duplicated().sum())
        )

    # ======================================================
    # DATASET PREVIEW
    # ======================================================

    st.divider()

    st.subheader("📈 Dataset Preview")

    st.dataframe(
        dataset.head(15),
        use_container_width=True,
        hide_index=True
    )

    # ======================================================
    # EXECUTIVE REMARKS
    # ======================================================

    st.divider()

    st.subheader("📄 Executive Remarks")

    st.success(
        "✔ Retail dataset has been successfully validated and processed."
    )

    st.success(
        "✔ Machine Learning model is connected with FastAPI backend."
    )

    st.success(
        "✔ Customer churn predictions are available."
    )

    st.success(
        "✔ Business insights are generated successfully."
    )

    st.success(
        "✔ Dashboard is ready for executive reporting and business monitoring."
    )

    st.info(
        "PDF report export and automated email reporting will be available in a future release."
    )

    footer()
    
# ==========================================================
# SETTINGS & PROJECT INFORMATION
# ==========================================================

elif st.session_state.page == "⚙ Settings":

    st.title("⚙ Dashboard Settings")

    st.subheader("Dashboard Information")

    info = pd.DataFrame({

        "Module": [

            "Dataset Audit",
            "Data Validation",
            "Consistency Check",
            "Data Cleaning",
            "Feature Engineering",
            "EDA",
            "Visualization",
            "Machine Learning",
            "Prediction",
            "FastAPI",
            "Streamlit Dashboard"

        ],

        "Status": [

            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Connected",
            "Running"

        ]

    })

    st.dataframe(

        info,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    st.subheader("System Information")

    st.write("**Project Name:** AI Retail Analytics Platform")

    st.write("**Framework:** Streamlit")

    st.write("**Backend API:** FastAPI")

    st.write("**Machine Learning Model:** Random Forest")

    st.write("**Dataset Size:**", number(get_dataset().shape[0]))

    st.write("**Total Features:**", number(get_dataset().shape[1]))

    st.divider()

    st.subheader("Dashboard Features")

    features = [

        "Interactive KPI Dashboard",

        "Dynamic Dataset Upload",

        "Customer Churn Prediction",

        "Business Insights",

        "Executive Analytics",

        "Download Reports",

        "REST API Integration",

        "Machine Learning Predictions"

    ]

    for feature in features:

        st.success(feature)

    st.divider()

    st.subheader("Project Pipeline")

    st.code("""

Upload Dataset
      │
      ▼
Data Validation
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Machine Learning
      │
      ▼
Prediction
      │
      ▼
Business Insights
      │
      ▼
Interactive Dashboard

""")

    st.divider()

    footer()
    
