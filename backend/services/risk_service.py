import os
import joblib
import pandas as pd
from typing import Dict, Any, List

# ---------------------------------------------------------
# Load Trained ML Model
# ---------------------------------------------------------

MODEL_PATH = os.path.join("ai", "models", "landslide_model.pkl")

try:
    model_data = joblib.load(MODEL_PATH)
    model = model_data["model"]
    FEATURES = model_data["features"]
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}: {e}")
    model = None
    FEATURES = []


# ---------------------------------------------------------
# Risk Level Categorization
# ---------------------------------------------------------

def get_risk_level(probability: float) -> str:
    """Convert a risk probability into a human-readable risk level."""
    if probability < 0.25:
        return "LOW"
    elif probability < 0.50:
        return "MODERATE"
    elif probability < 0.75:
        return "HIGH"
    else:
        return "CRITICAL"


# ---------------------------------------------------------
# Generate Risk Explanations
# ---------------------------------------------------------

def generate_explanation(
    rainfall_24h: float,
    soil_moisture: float,
    slope: float,
    historical_landslides: int
) -> List[Dict[str, Any]]:
    """Generates structured list of high-impact environmental risk factors."""
    factors = []

    if rainfall_24h >= 50:
        factors.append({
            "factor": "24-hour rainfall",
            "effect": "increased risk",
            "severity": "HIGH"
        })

    if soil_moisture >= 0.7:
        factors.append({
            "factor": "soil moisture",
            "effect": "increased risk",
            "severity": "HIGH"
        })

    if slope >= 30:
        factors.append({
            "factor": "slope",
            "effect": "increased risk",
            "severity": "HIGH"
        })
    elif slope >= 15:
        factors.append({
            "factor": "slope",
            "effect": "increased risk",
            "severity": "MODERATE"
        })

    if historical_landslides > 0:
        factors.append({
            "factor": "historical landslides",
            "effect": "increased risk",
            "severity": "HIGH"
        })

    return factors if factors else [{"factor": "baseline", "effect": "normal conditions", "severity": "LOW"}]


# ---------------------------------------------------------
# Orchestrated Risk Analysis Pipeline (Using Trained Model)
# ---------------------------------------------------------

def analyze_risk(
    rainfall_24h: float,
    rainfall_7d: float,
    soil_moisture: float,
    slope: float,
    elevation: float,
    historical_landslides: int
) -> Dict[str, Any]:
    """Runs input data through the trained machine learning model."""
    if model is None:
        raise RuntimeError("Trained machine learning model is not loaded.")

    # Map API inputs to the exact feature names expected by your trained model
    input_dict = {
        "Rainfall_mm": rainfall_24h,
        "Slope_Angle": slope,
        "Soil_Saturation": soil_moisture,
        "Vegetation_Cover": 0.50,    # Default placeholder or pass through if available
        "Earthquake_Activity": 0,    # Default placeholder
        "Proximity_to_Water": 0.30,  # Default placeholder
        "Soil_Type_Gravel": 1,       # Default categorical encoding
        "Soil_Type_Sand": 0,
        "Soil_Type_Silt": 0
    }

    # Convert to DataFrame and align features
    input_df = pd.DataFrame([input_dict])
    for feature in FEATURES:
        if feature not in input_df.columns:
            input_df[feature] = 0.0
    input_df = input_df[FEATURES]

    # Get probability and prediction from the model
    probability = float(model.predict_proba(input_df)[0][1])
    level = get_risk_level(probability)

    factors = generate_explanation(
        rainfall_24h=rainfall_24h,
        soil_moisture=soil_moisture,
        slope=slope,
        historical_landslides=historical_landslides
    )

    return {
        "risk_score": round(probability, 4),
        "risk_level": level,
        "confidence": round(float(model.predict(input_df)[0]), 2),
        "factors": factors
    }