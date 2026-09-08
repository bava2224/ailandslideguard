from typing import Dict, Any


# ---------------------------------------------------------
# Risk level
# ---------------------------------------------------------

def get_risk_level(score: float) -> str:
    """
    Convert a risk score into a risk level.
    """

    if score >= 0.85:
        return "CRITICAL"

    if score >= 0.70:
        return "HIGH"

    if score >= 0.40:
        return "MODERATE"

    return "LOW"


# ---------------------------------------------------------
# Calculate environmental risk
# ---------------------------------------------------------

def calculate_environmental_risk(
    rainfall_24h: float,
    rainfall_7d: float,
    soil_moisture: float,
    slope: float,
    elevation: float,
    historical_landslides: int
) -> float:
    """
    Prototype environmental risk calculation.

    NOTE:
    This is NOT the final ML model.
    The final system is intended to use XGBoost.
    """

    score = 0.0

    # Rainfall
    if rainfall_24h >= 100:
        score += 0.30
    elif rainfall_24h >= 50:
        score += 0.20
    else:
        score += 0.10

    # Previous 7-day rainfall
    if rainfall_7d >= 300:
        score += 0.10
    elif rainfall_7d >= 150:
        score += 0.05

    # Soil moisture
    score += soil_moisture * 0.20

    # Slope
    if slope >= 30:
        score += 0.25
    elif slope >= 15:
        score += 0.15
    else:
        score += 0.05

    # Historical landslides
    if historical_landslides > 0:
        score += 0.15

    return min(score, 1.0)


# ---------------------------------------------------------
# Generate explanation
# ---------------------------------------------------------

def generate_explanation(
    rainfall_24h: float,
    soil_moisture: float,
    slope: float,
    historical_landslides: int
) -> list[Dict[str, Any]]:

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

    return factors


# ---------------------------------------------------------
# Complete risk analysis
# ---------------------------------------------------------

def analyze_risk(
    rainfall_24h: float,
    rainfall_7d: float,
    soil_moisture: float,
    slope: float,
    elevation: float,
    historical_landslides: int
) -> Dict[str, Any]:

    score = calculate_environmental_risk(
        rainfall_24h=rainfall_24h,
        rainfall_7d=rainfall_7d,
        soil_moisture=soil_moisture,
        slope=slope,
        elevation=elevation,
        historical_landslides=historical_landslides
    )

    level = get_risk_level(score)

    factors = generate_explanation(
        rainfall_24h=rainfall_24h,
        soil_moisture=soil_moisture,
        slope=slope,
        historical_landslides=historical_landslides
    )

    return {
        "risk_score": round(score, 3),
        "risk_level": level,
        "confidence": 0.80,
        "factors": factors
    }