import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

def page_config():

    st.set_page_config(
        page_title="AI Retail Analytics Platform",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ==========================================================
# HEADER
# ==========================================================

def page_header():

    st.title("📊 AI Retail Analytics & Customer Intelligence Platform")

    st.caption(
        "End-to-End Retail Analytics | Machine Learning | Business Intelligence | FastAPI | Streamlit"
    )

    st.divider()

# ==========================================================
# API STATUS
# ==========================================================

def api_status(status):

    if status is None:

        st.error("🔴 API Offline")

        return

    if status["status"] == "running":

        st.success("🟢 API Connected")

    else:

        st.error("🔴 API Offline")

# ==========================================================
# KPI CARD
# ==========================================================

def kpi_card(title, value):

    st.metric(
        label=title,
        value=value
    )

# ==========================================================
# HEALTH SCORE
# ==========================================================

def health_score(score):

    st.subheader("Dataset Health Score")

    st.progress(score / 100)

    st.write(f"**{score}/100**")

# ==========================================================
# RISK METER
# ==========================================================

def risk_meter(probability):

    st.subheader("Prediction Confidence")

    st.progress(probability)

    st.write(f"{probability*100:.2f}%")

# ==========================================================
# SECTION TITLE
# ==========================================================

def section(title):

    st.markdown(f"## {title}")

# ==========================================================
# SUCCESS CARD
# ==========================================================

def success_box(message):

    st.success(message)

# ==========================================================
# WARNING CARD
# ==========================================================

def warning_box(message):

    st.warning(message)

# ==========================================================
# ERROR CARD
# ==========================================================

def error_box(message):

    st.error(message)

# ==========================================================
# INFO CARD
# ==========================================================

def info_box(message):

    st.info(message)

# ==========================================================
# RECOMMENDATION CARD
# ==========================================================

def recommendation(title, message):

    st.markdown(
        f"""
### 💡 {title}

{message}
"""
    )

# ==========================================================
# PIPELINE STATUS
# ==========================================================

def pipeline_status():

    st.markdown("### ⚙ Pipeline Status")

    st.success("✔ Dataset Loaded")

    st.success("✔ Data Validated")

    st.success("✔ Data Cleaned")

    st.success("✔ Feature Engineering Completed")

    st.success("✔ Model Loaded")

    st.success("✔ Predictions Ready")

    st.success("✔ Dashboard Ready")

# ==========================================================
# DOWNLOAD BUTTON
# ==========================================================

def download_button(df, filename):

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="⬇ Download CSV",

        data=csv,

        file_name=filename,

        mime="text/csv"

    )

# ==========================================================
# FOOTER
# ==========================================================

def footer():

    st.divider()

    st.caption("━━━━━━━━━━━━━━━━━━━━━━")

    st.markdown("**AI Retail Analytics Platform**")

    st.caption("Powered by Streamlit • FastAPI • Scikit-Learn")

    st.caption("Version 1.0")