"""
Run this ONCE to train and save the churn prediction model.

Steps:
1. Download the Telco Customer Churn dataset from Kaggle:
   https://www.kaggle.com/datasets/blastchar/telco-customer-churn
2. Save the file as: ml/sample_data/churn_data.csv
3. Run: python ml/train_churn.py
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

DATA_PATH  = "ml/sample_data/churn_data.csv"
MODEL_PATH = "ml/churn_model.pkl"

FEATURES = [
    "tenure", "MonthlyCharges", "TotalCharges",
    "Contract", "PaymentMethod", "InternetService"
]


def train():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)

    # Drop customer ID — not a feature
    df = df.drop(columns=["customerID"], errors="ignore")

    # Fix TotalCharges (contains spaces in raw Kaggle data)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Encode target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = df.dropna(subset=["Churn", "TotalCharges"])

    features = [f for f in FEATURES if f in df.columns]
    print(f"Using features: {features}")

    X = df[features].copy()
    y = df["Churn"]

    # Encode categorical columns
    for col in X.select_dtypes(include="object").columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    X = X.fillna(X.median(numeric_only=True))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training on {len(X_train)} rows, testing on {len(X_test)} rows...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n" + "=" * 50)
    print("MODEL EVALUATION")
    print("=" * 50)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Stay", "Churn"]))
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nFeature Importances:")
    for feat, imp in sorted(
        zip(features, model.feature_importances_), key=lambda x: -x[1]
    ):
        print(f"  {feat}: {imp:.4f}")

    os.makedirs("ml", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\n✅ Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()
