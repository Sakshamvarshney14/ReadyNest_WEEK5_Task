import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ==========================================================
# PATHS
# ==========================================================

DATA_PATH = "data/processed/feature_engineered_data.csv"

MODEL_DIR = "models"

REPORT_DIR = "reports"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(DATA_PATH)

print("="*70)
print("MODEL TRAINING")
print("="*70)

# ==========================================================
# TARGET
# ==========================================================

df["ChurnStatus"] = df["ChurnStatus"].map({
    "No":0,
    "Yes":1
})

# ==========================================================
# FEATURES
# ==========================================================

drop_columns = [

    "TransactionID",

    "CustomerID",

    "PurchaseDate",

    "ChurnStatus"

]

X = df.drop(columns=drop_columns)

y = df["ChurnStatus"]

# ==========================================================
# NUMERIC / CATEGORICAL
# ==========================================================

numeric_features = X.select_dtypes(
    include=["int64","float64"]
).columns

categorical_features = X.select_dtypes(
    include=["object","category"]
).columns

# ==========================================================
# PREPROCESSOR
# ==========================================================

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
# MODEL
# ==========================================================

model = RandomForestClassifier(

    n_estimators=200,

    random_state=42

)

pipeline = Pipeline(

    steps=[

        ("preprocessor",preprocessor),

        ("model",model)

    ]

)

# ==========================================================
# SPLIT
# ==========================================================

X_train,X_test,y_train,y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)

# ==========================================================
# TRAIN
# ==========================================================

pipeline.fit(

    X_train,

    y_train

)

pred = pipeline.predict(

    X_test

)

accuracy = accuracy_score(

    y_test,

    pred

)

print(f"\nAccuracy : {accuracy:.4f}")

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

# Get transformed feature names
feature_names = pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()

# Get feature importance from Random Forest
importances = pipeline.named_steps[
    "model"
].feature_importances_

# Create feature importance dataframe
feature_importance_df = pd.DataFrame({

    "Feature": feature_names,

    "Importance": importances

})

# Sort by importance
feature_importance_df = feature_importance_df.sort_values(

    by="Importance",

    ascending=False

)

# Save feature importance
feature_importance_df.to_csv(

    "reports/feature_importance.csv",

    index=False

)

print("\nTop Feature Importance:")

print(

    feature_importance_df.head(10)

)

# ==========================================================
# SAVE MODEL
# ==========================================================

joblib.dump(

    pipeline,

    "models/best_model.pkl"

)

with open(

    "reports/model_training_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("="*60+"\n")

    f.write("MODEL TRAINING REPORT\n")

    f.write("="*60+"\n\n")

    f.write(f"Rows : {len(df)}\n")

    f.write(f"Columns : {len(df.columns)}\n")

    f.write(f"Accuracy : {accuracy:.4f}\n")

print("\nModel Saved Successfully")

print("models/best_model.pkl")

print("\nTraining Report Saved")

print("reports/model_training_report.txt")