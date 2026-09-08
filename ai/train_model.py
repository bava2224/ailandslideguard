import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier


# -----------------------------
# CONFIGURATION
# -----------------------------

DATA_PATH = "ai/data/landslide_dataset.csv"
MODEL_PATH = "ai/models/landslide_model.pkl"


# Features used by the model
FEATURES = [
    "Rainfall_mm",
    "Slope_Angle",
    "Soil_Saturation",
    "Vegetation_Cover",
    "Earthquake_Activity",
    "Proximity_to_Water",
    "Soil_Type_Gravel",
    "Soil_Type_Sand",
    "Soil_Type_Silt"
]

TARGET = "Landslide"


# -----------------------------
# LOAD DATA
# -----------------------------

def load_data():

    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully!")
    print("Dataset shape:", df.shape)

    return df


# -----------------------------
# PREPROCESS DATA
# -----------------------------

def preprocess_data(df):

    print("Preprocessing data...")

    # Keep only required columns
    df = df[FEATURES + [TARGET]]

    # Remove missing values
    df = df.dropna()

    X = df[FEATURES]
    y = df[TARGET]

    return X, y


# -----------------------------
# TRAIN MODEL
# -----------------------------

def train_model():

    # Load dataset
    df = load_data()

    # Preprocess
    X, y = preprocess_data(df)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Training XGBoost model...")

    # Create model
    model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        eval_metric="logloss"
    )

    # Train model
    model.fit(X_train, y_train)

    print("Model training completed!")

    # -----------------------------
    # EVALUATION
    # -----------------------------

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)

    print("\nModel Performance")
    print("-" * 30)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    try:
        roc_auc = roc_auc_score(y_test, probabilities)
        print(f"ROC-AUC:   {roc_auc:.4f}")
    except ValueError:
        print("ROC-AUC could not be calculated.")

    # -----------------------------
    # SAVE MODEL
    # -----------------------------

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "features": FEATURES
        },
        MODEL_PATH
    )

    print(f"\nModel saved successfully at: {MODEL_PATH}")


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    train_model()