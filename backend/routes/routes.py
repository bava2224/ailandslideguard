# backend/routes/routes.py
import math
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.landslide_model import LandslideDataModel

router = APIRouter(
    prefix="/api/v1/routes",
    tags=["Route Risk"]
)

# ---------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------
class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class RouteAnalysisRequest(BaseModel):
    origin: Location
    destination: Location

# ---------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------
class RouteAnalysisResponse(BaseModel):
    risk_score: float
    risk_level: str
    exposed_percentage: float
    dangerous_segments: List[Dict[str, Any]]
    recommendation: str

# ---------------------------------------------------------
# Distance Helper (Haversine Formula in KM)
# ---------------------------------------------------------
def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ---------------------------------------------------------
# Route Analysis Endpoint
# ---------------------------------------------------------
@router.post("/analyze", response_model=RouteAnalysisResponse)
def analyze_route(
    request: RouteAnalysisRequest,
    db: Session = Depends(get_db)
):
    # Fetch all dynamic hazard zones from SQLite
    active_hazards = db.query(LandslideDataModel).all()

    dangerous_segments = []
    max_risk_score = 0.0

    # Evaluate proximity against active landslide points in DB
    for hazard in active_hazards:
        if hazard.latitude is None or hazard.longitude is None:
            continue

        # Distance from origin and destination to active hazard
        dist_to_origin = haversine(request.origin.latitude, request.origin.longitude, hazard.latitude, hazard.longitude)
        dist_to_dest = haversine(request.destination.latitude, request.destination.longitude, hazard.latitude, hazard.longitude)

        # Consider zone critical if within 20 km threshold
        min_dist = min(dist_to_origin, dist_to_dest)
        if min_dist <= 20.0:
            score = 0.85 if hazard.risk_level.lower() == "high" else 0.50
            if score > max_risk_score:
                max_risk_score = score

            dangerous_segments.append({
                "segment_id": f"ZONE_{hazard.id}",
                "location": hazard.location,
                "distance_km": round(min_dist, 2),
                "risk_score": score,
                "risk_level": hazard.risk_level.upper()
            })

    # Default fallback values if no database records are in range
    if not dangerous_segments:
        risk_score = 0.10
        risk_level = "LOW"
        exposed_percentage = 0.0
        recommendation = "Route clear: No active high-risk landslide zones detected near path."
    else:
        risk_score = max_risk_score
        risk_level = "CRITICAL" if max_risk_score >= 0.8 else "HIGH"
        exposed_percentage = min(len(dangerous_segments) * 12.5, 100.0)
        recommendation = "Caution: Planned route contains high-risk landslide zones. Check local bulletins before travel."

    return RouteAnalysisResponse(
        risk_score=risk_score,
        risk_level=risk_level,
        exposed_percentage=exposed_percentage,
        dangerous_segments=dangerous_segments,
        recommendation=recommendation
    )