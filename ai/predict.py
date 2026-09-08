import joblib
import pandas as pd


# Path to the trained model
MODEL_PATH = "ai/models/landslide_model.pkl"


# Load model
model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
FEATURES = model_data["features"]


def get_risk_level(probability):
    """
    Convert probability into a risk level.
    """

    if probability < 0.25:
        return "LOW"

    elif probability < 0.50:
        return "MODERATE"

    elif probability < 0.75:
        return "HIGH"

    else:
        return "CRITICAL"


def predict_landslide(data):
    """
    Predict landslide risk based on input data.
    """

    # Convert input dictionary to DataFrame
    input_data = pd.DataFrame([data])

    # Ensure correct feature order
    input_data = input_data[FEATURES]

    # Get landslide probability
    probability = model.predict_proba(input_data)[0][1]

    # Get prediction
    prediction = model.predict(input_data)[0]

    # Get risk level
    risk_level = get_risk_level(probability)

    return {
        "landslide_prediction": int(prediction),
        "risk_probability": round(float(probability), 4),
        "risk_percentage": round(float(probability) * 100, 2),
        "risk_level": risk_level
    }


# Test prediction
if __name__ == "__main__":

    sample_data = {
        "Rainfall_mm": 120,
        "Slope_Angle": 35,
        "Soil_Saturation": 0.75,
        "Vegetation_Cover": 0.50,
        "Earthquake_Activity": 0,
        "Proximity_to_Water": 0.30,
        "Soil_Type_Gravel": 1,
        "Soil_Type_Sand": 0,
        "Soil_Type_Silt": 0
    }

    result = predict_landslide(sample_data)

    print(result)


