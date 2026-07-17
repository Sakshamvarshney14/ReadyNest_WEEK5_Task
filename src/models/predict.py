import os
import joblib
import pandas as pd

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = "data/processed/feature_engineered_data.csv"
MODEL_PATH = "models/best_model.pkl"

OUTPUT_DIR = "data/predictions"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "predictions.csv"
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATA_PATH)

original_df = df.copy()

# ==========================================================
# PREPARE FEATURES
# ==========================================================

features = df.drop(
    columns=[
        "TransactionID",
        "CustomerID",
        "PurchaseDate",
        "ChurnStatus"
    ]
)

# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load(MODEL_PATH)

# ==========================================================
# PREDICTION
# ==========================================================

prediction = model.predict(features)

probability = model.predict_proba(features)[:,1]

# ==========================================================
# CONVERT LABELS
# ==========================================================

prediction_label = [
    "Yes" if x == 1 else "No"
    for x in prediction
]

# ==========================================================
# ADD COLUMNS
# ==========================================================

original_df["PredictedChurn"] = prediction_label

original_df["PredictionProbability"] = (
    probability * 100
).round(2)

original_df["PredictionConfidence"] = original_df[
    "PredictionProbability"
].apply(

    lambda x:
        "High"
        if x >= 80
        else
        "Medium"
        if x >= 60
        else
        "Low"

)

original_df["PredictionCorrect"] = (
    original_df["ChurnStatus"] ==
    original_df["PredictedChurn"]
)

# ==========================================================
# SAVE CSV
# ==========================================================

original_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ==========================================================
# SUMMARY
# ==========================================================

print("="*70)
print("PREDICTION SUMMARY")
print("="*70)

print(f"Total Records : {len(original_df)}")

print(
    f"Predicted Churn : "
    f"{(original_df['PredictedChurn']=='Yes').sum()}"
)

print(
    f"Predicted Non-Churn : "
    f"{(original_df['PredictedChurn']=='No').sum()}"
)

print()

print(
    original_df["PredictionConfidence"]
    .value_counts()
)

print()

print(
    f"Prediction Accuracy : "
    f"{original_df['PredictionCorrect'].mean()*100:.2f}%"
)

print()

print("Prediction File Saved")

print(OUTPUT_FILE)

print("="*70)