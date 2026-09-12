from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.risk_service import analyze_risk


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/v1/prediction",
    tags=["Prediction"]
)


# --------------------------------------------------------
# Request Schema
# ---------------------------------------------------------

class PredictionRequest(BaseModel):
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

    rainfall_24h: float = Field(
        ...,
        ge=0
    )

    rainfall_7d: float = Field(
        ...,
        ge=0
    )

    soil_moisture: float = Field(
        ...,
        ge=0,
        le=1
    )

    slope: float = Field(
        ...,
        ge=0
    )

    elevation: float = Field(
        ...,
        ge=0
    )

    historical_landslides: int = Field(
        default=0,
        ge=0
    )


# ---------------------------------------------------------
# Response Schema
# ---------------------------------------------------------

class PredictionResponse(BaseModel):

    id: int

    latitude: float
    longitude: float

    risk_score: float

    risk_level: str

    confidence: float

    prediction_time: datetime

    factors: list[dict]


# ---------------------------------------------------------
# Temporary storage
# ---------------------------------------------------------
# This will later be replaced with PostgreSQL/PostGIS.

predictions_db: list[PredictionResponse] = []

next_prediction_id = 1


# ---------------------------------------------------------
# Create Prediction
# ---------------------------------------------------------

@router.post(
    "",
    response_model=PredictionResponse,
    status_code=201
)
def create_prediction(
    data: PredictionRequest
):

    global next_prediction_id

    try:

        # ---------------------------------------------
        # Send environmental data to risk service
        # ---------------------------------------------

        result = analyze_risk(

            rainfall_24h=data.rainfall_24h,

            rainfall_7d=data.rainfall_7d,

            soil_moisture=data.soil_moisture,

            slope=data.slope,

            elevation=data.elevation,

            historical_landslides=data.historical_landslides
        )

        # ---------------------------------------------
        # Create prediction response
        # ---------------------------------------------

        prediction = PredictionResponse(

            id=next_prediction_id,

            latitude=data.latitude,

            longitude=data.longitude,

            risk_score=result["risk_score"],

            risk_level=result["risk_level"],

            confidence=result["confidence"],

            prediction_time=datetime.utcnow(),

            factors=result["factors"]
        )

        # ---------------------------------------------
        # Store prediction temporarily
        # ---------------------------------------------

        predictions_db.append(prediction)

        next_prediction_id += 1

        return prediction

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )


# ---------------------------------------------------------
# Get All Predictions
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[PredictionResponse]
)
def get_predictions():

    return predictions_db


# ---------------------------------------------------------
# Get Prediction by ID
# ---------------------------------------------------------

@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse
)
def get_prediction(
    prediction_id: int
):

    for prediction in predictions_db:

        if prediction.id == prediction_id:

            return prediction

    raise HTTPException(
        status_code=404,
        detail="Prediction not found"
    )