import math
from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import LandslideData


router = APIRouter(
    prefix="/api/v1/routes",
    tags=["Route Risk"]
)


class LocationPoint(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class RouteAnalysisRequest(BaseModel):
    origin: LocationPoint
    destination: LocationPoint


class RouteAnalysisResponse(BaseModel):
    safe: bool
    risk_level: str
    distance_km: float
    warnings: List[str]
    hazards: List[Dict[str, Any]]


def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calculate approximate distance between two coordinates in kilometres.
    """

    earth_radius_km = 6371

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(earth_radius_km * c, 2)


@router.post("/analyze", response_model=RouteAnalysisResponse)
def analyze_route(
    request: RouteAnalysisRequest,
    db: Session = Depends(get_db)
):
    active_hazards = db.query(LandslideData).all()

    distance_km = calculate_distance(
        request.origin.latitude,
        request.origin.longitude,
        request.destination.latitude,
        request.destination.longitude
    )

    nearby_hazards = []
    warnings = []

    for hazard in active_hazards:
        if hazard.latitude is None or hazard.longitude is None:
            continue

        hazard_distance = calculate_distance(
            request.origin.latitude,
            request.origin.longitude,
            hazard.latitude,
            hazard.longitude
        )

        if hazard_distance <= 50:
            nearby_hazards.append({
                "id": hazard.id,
                "location": hazard.location,
                "latitude": hazard.latitude,
                "longitude": hazard.longitude,
                "risk_level": hazard.risk_level,
                "distance_from_origin_km": round(hazard_distance, 2)
            })

            warnings.append(
                f"{hazard.risk_level} risk detected near {hazard.location}"
            )

    risk_levels = [
        str(hazard["risk_level"]).lower()
        for hazard in nearby_hazards
    ]

    if "high" in risk_levels:
        risk_level = "HIGH"
        safe = False
    elif "medium" in risk_levels:
        risk_level = "MEDIUM"
        safe = False
    elif "low" in risk_levels:
        risk_level = "LOW"
        safe = True
    else:
        risk_level = "SAFE"
        safe = True

    return RouteAnalysisResponse(
        safe=safe,
        risk_level=risk_level,
        distance_km=distance_km,
        warnings=warnings,
        hazards=nearby_hazards
    )