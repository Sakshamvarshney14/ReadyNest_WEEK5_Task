import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    classification_report
)

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = "data/processed/feature_engineered_data.csv"
MODEL_PATH = "models/best_model.pkl"

REPORT_DIR = "reports"
FIGURE_DIR = "reports/figures"

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATA_PATH)

df["ChurnStatus"] = df["ChurnStatus"].map({
    "No": 0,
    "Yes": 1
})

drop_columns = [
    "TransactionID",
    "CustomerID",
    "PurchaseDate",
    "ChurnStatus"
]

X = df.drop(columns=drop_columns)
y = df["ChurnStatus"]

# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load(MODEL_PATH)

# ==========================================================
# PREDICTION
# ==========================================================

pred = model.predict(X)
prob = model.predict_proba(X)[:,1]

# ==========================================================
# METRICS
# ==========================================================

accuracy = accuracy_score(y,pred)
precision = precision_score(y,pred)
recall = recall_score(y,pred)
f1 = f1_score(y,pred)
roc = roc_auc_score(y,prob)

print("="*70)
print("MODEL EVALUATION")
print("="*70)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {roc:.4f}")

# ==========================================================
# CLASSIFICATION REPORT
# ==========================================================

class_report = classification_report(y,pred)

# ==========================================================
# CONFUSION MATRIX
# ==========================================================

cm = confusion_matrix(y,pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

disp.plot()

plt.title("Confusion Matrix")

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURE_DIR,
        "confusion_matrix.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# ROC CURVE
# ==========================================================

RocCurveDisplay.from_predictions(
    y,
    prob
)

plt.title("ROC Curve")

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURE_DIR,
        "roc_curve.png"
    ),
    dpi=300
)

plt.close()

# ==========================================================
# SAVE REPORT
# ==========================================================

with open(
    os.path.join(
        REPORT_DIR,
        "model_evaluation_report.txt"
    ),
    "w",
    encoding="utf-8"
) as f:

    f.write("="*70+"\n")
    f.write("MODEL EVALUATION REPORT\n")
    f.write("="*70+"\n\n")

    f.write(f"Accuracy  : {accuracy:.4f}\n")
    f.write(f"Precision : {precision:.4f}\n")
    f.write(f"Recall    : {recall:.4f}\n")
    f.write(f"F1 Score  : {f1:.4f}\n")
    f.write(f"ROC AUC   : {roc:.4f}\n\n")

    f.write("Classification Report\n")
    f.write("-"*70+"\n")
    f.write(class_report)

print("\nEvaluation Report Saved")
print("reports/model_evaluation_report.txt")

print("\nConfusion Matrix Saved")
print("reports/figures/confusion_matrix.png")

print("\nROC Curve Saved")
print("reports/figures/roc_curve.png")

print("\nEvaluation Completed Successfully")