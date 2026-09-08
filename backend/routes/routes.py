from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/v1/routes",
    tags=["Route Risk"]
)


# ---------------------------------------------------------
# Request
# ---------------------------------------------------------

class Location(BaseModel):

    latitude: float = Field(
        ...,
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180
    )


class RouteAnalysisRequest(BaseModel):

    origin: Location

    destination: Location


# ---------------------------------------------------------
# Response
# ---------------------------------------------------------

class RouteAnalysisResponse(BaseModel):

    risk_score: float

    risk_level: str

    exposed_percentage: float

    dangerous_segments: list[dict]

    recommendation: str


# ---------------------------------------------------------
# Route analysis
# ---------------------------------------------------------

@router.post(
    "/analyze",
    response_model=RouteAnalysisResponse
)
def analyze_route(
    request: RouteAnalysisRequest
):

    # -----------------------------------------------------
    # DEMO ONLY
    #
    # In the final system:
    #
    # 1. Get route from Google Maps
    # 2. Obtain route geometry
    # 3. Split route into segments
    # 4. Check each segment against PostGIS risk zones
    # 5. Calculate exposure
    # ----------------------------------------------------

    # Temporary demo values

    exposed_percentage = 18.5

    risk_score = 0.72

    risk_level = "HIGH"

    dangerous_segments = [

        {
            "segment_id": "SEGMENT_03",
            "risk_score": 0.88,
            "risk_level": "CRITICAL"
        },

        {
            "segment_id": "SEGMENT_04",
            "risk_score": 0.76,
            "risk_level": "HIGH"
        }

    ]

    recommendation = (
        "Caution: planned route contains "
        "high-risk landslide zones."
    )

    return RouteAnalysisResponse(

        risk_score=risk_score,

        risk_level=risk_level,

        exposed_percentage=exposed_percentage,

        dangerous_segments=dangerous_segments,

        recommendation=recommendation
    )