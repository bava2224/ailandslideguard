# backend/routes/landslides.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_landslides():
    """
    Fetch all active landslide hazard zones for spatial visualization.
    """
    return [
        { "id": 1, "location": "Zone A - Shillong Hills", "risk_level": "High", "latitude": 25.5788, "longitude": 91.8933, "rainfall": 110.5, "soil_moisture": 0.78 },
        { "id": 2, "location": "Zone B - Kohima Slopes", "risk_level": "Critical", "latitude": 25.6751, "longitude": 94.1086, "rainfall": 145.0, "soil_moisture": 0.89 },
        { "id": 3, "location": "Zone C - Itanagar Ridge", "risk_level": "Moderate", "latitude": 27.0844, "longitude": 93.6053, "rainfall": 62.0, "soil_moisture": 0.55 },
        { "id": 4, "location": "Zone D - Aizawl Basin", "risk_level": "Low", "latitude": 23.7271, "longitude": 92.7176, "rainfall": 18.2, "soil_moisture": 0.32 }
    ]