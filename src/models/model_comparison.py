import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = "data/processed/feature_engineered_data.csv"

os.makedirs("reports", exist_ok=True)
os.makedirs("models", exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATA_PATH)

df["ChurnStatus"] = df["ChurnStatus"].map({
    "No":0,
    "Yes":1
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
# FEATURES
# ==========================================================

numeric_features = X.select_dtypes(
    include=["int64","float64"]
).columns

categorical_features = X.select_dtypes(
    include=["object","category","string"]
).columns

numeric_transformer = Pipeline(
    steps=[
        ("imputer",SimpleImputer(strategy="median"))
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer",SimpleImputer(strategy="most_frequent")),
        ("encoder",OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num",numeric_transformer,numeric_features),
        ("cat",categorical_transformer,categorical_features)
    ]
)

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================================================
# MODELS
# ==========================================================

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Random Forest":
        RandomForestClassifier(
            random_state=42,
            n_estimators=200
        ),

    "Gradient Boosting":
        GradientBoostingClassifier(
            random_state=42
        )

}

results = []

best_accuracy = 0
best_pipeline = None
best_name = ""

print("="*70)
print("MODEL COMPARISON")
print("="*70)

for name,model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor",preprocessor),
            ("model",model)
        ]
    )

    pipeline.fit(X_train,y_train)

    pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test,pred)
    pre = precision_score(y_test,pred)
    rec = recall_score(y_test,pred)
    f1 = f1_score(y_test,pred)

    results.append({

        "Model":name,

        "Accuracy":round(acc,4),

        "Precision":round(pre,4),

        "Recall":round(rec,4),

        "F1 Score":round(f1,4)

    })

    print(f"\n{name}")

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {pre:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")

    if acc > best_accuracy:

        best_accuracy = acc
        best_pipeline = pipeline
        best_name = name

# ==========================================================
# SAVE RESULTS
# ==========================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    "reports/model_comparison.csv",
    index=False
)

joblib.dump(
    best_pipeline,
    "models/best_model.pkl"
)

print("\n"+"="*70)

print(f"BEST MODEL : {best_name}")

print(f"Accuracy   : {best_accuracy:.4f}")

print("="*70)

print("\nComparison Report Saved")

print("reports/model_comparison.csv")

print("\nBest Model Saved")

print("models/best_model.pkl")