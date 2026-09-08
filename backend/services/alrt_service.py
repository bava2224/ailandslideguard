from typing import Dict, Any, Optional


# ---------------------------------------------------------
# Alert thresholds
# ---------------------------------------------------------

ALERT_THRESHOLDS = {
    "LOW": 0.40,
    "MODERATE": 0.40,
    "HIGH": 0.70,
    "CRITICAL": 0.85
}


# ---------------------------------------------------------
# Determine alert level
# ---------------------------------------------------------

def determine_alert_level(risk_score: float) -> str:
    """
    Convert risk score into an alert level.
    """

    if risk_score >= ALERT_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"

    if risk_score >= ALERT_THRESHOLDS["HIGH"]:
        return "HIGH"

    if risk_score >= ALERT_THRESHOLDS["MODERATE"]:
        return "MODERATE"

    return "LOW"


# ---------------------------------------------------------
# Check whether alert should be generated
# ---------------------------------------------------------

def should_generate_alert(
    risk_score: float,
    previous_score: Optional[float] = None
) -> bool:
    """
    Determine whether a new alert should be generated.

    A new alert is generated when the current score
    crosses an important threshold.
    """

    current_level = determine_alert_level(risk_score)

    if current_level in ["HIGH", "CRITICAL"]:

        if previous_score is None:
            return True

        previous_level = determine_alert_level(
            previous_score
        )

        # Alert only when the level increases
        if current_level != previous_level:
            return True

    return False


# ---------------------------------------------------------
# Create alert information
# ---------------------------------------------------------

def create_alert_data(
    latitude: float,
    longitude: float,
    risk_score: float,
    reason: str = "Landslide risk threshold exceeded"
) -> Dict[str, Any]:

    level = determine_alert_level(risk_score)

    if level == "CRITICAL":
        title = "Critical Landslide Risk"

    elif level == "HIGH":
        title = "High Landslide Risk"

    elif level == "MODERATE":
        title = "Moderate Landslide Risk"

    else:
        title = "Low Landslide Risk"

    return {
        "latitude": latitude,
        "longitude": longitude,
        "risk_score": round(risk_score, 3),
        "level": level,
        "title": title,
        "message": reason,
        "source": "risk_engine"
    }


# ---------------------------------------------------------
# Complete alert evaluation
# ---------------------------------------------------------

def evaluate_alert(
    latitude: float,
    longitude: float,
    risk_score: float,
    previous_score: Optional[float] = None
) -> Optional[Dict[str, Any]]:
    """
    Evaluate risk and return alert data if required.
    """

    if not should_generate_alert(
        risk_score,
        previous_score
    ):
        return None

    return create_alert_data(
        latitude=latitude,
        longitude=longitude,
        risk_score=risk_score
    )