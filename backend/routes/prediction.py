# backend/routes/prediction.py

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.services.risk_service import analyze_risk
from database.database import get_db
from database.models import LandslideData


router = APIRouter(
    prefix="/api/v1/prediction",
    tags=["Prediction"]
)


class PredictionRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    rainfall_24h: float = Field(..., ge=0)
    rainfall_7d: float = Field(..., ge=0)
    soil_moisture: float = Field(..., ge=0, le=1)
    slope: float = Field(..., ge=0)
    elevation: float = Field(..., ge=0)
    historical_landslides: int = Field(default=0, ge=0)


class PredictionResponse(BaseModel):
    id: int
    latitude: float
    longitude: float
    risk_score: float
    risk_level: str
    confidence: float
    prediction_time: datetime
    factors: list[dict]

    class Config:
        from_attributes = True


@router.post("", response_model=PredictionResponse, status_code=201)
def create_prediction(
    data: PredictionRequest,
    db: Session = Depends(get_db)
):
    try:
        result = analyze_risk(
            rainfall_24h=data.rainfall_24h,
            rainfall_7d=data.rainfall_7d,
            soil_moisture=data.soil_moisture,
            slope=data.slope,
            elevation=data.elevation,
            historical_landslides=data.historical_landslides
        )

        current_time = datetime.now(timezone.utc)

        db_record = LandslideData(
            location="Prediction",
            latitude=data.latitude,
            longitude=data.longitude,
            rainfall=data.rainfall_24h,
            soil_moisture=data.soil_moisture,
            risk_level=result["risk_level"],
            created_at=current_time
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return {
            "id": db_record.id,
            "latitude": db_record.latitude,
            "longitude": db_record.longitude,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "confidence": result["confidence"],
            "prediction_time": current_time,
            "factors": result["factors"]
        }

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Prediction persistence failed: {str(error)}"
        )


@router.get("", response_model=list[PredictionResponse])
def get_predictions(db: Session = Depends(get_db)):
    records = db.query(LandslideData).all()

    return [
        {
            "id": record.id,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "risk_score": 0.0,
            "risk_level": record.risk_level,
            "confidence": 0.0,
            "prediction_time": record.created_at,
            "factors": []
        }
        for record in records
    ]


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    record = (
        db.query(LandslideData)
        .filter(LandslideData.id == prediction_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return {
        "id": record.id,
        "latitude": record.latitude,
        "longitude": record.longitude,
        "risk_score": 0.0,
        "risk_level": record.risk_level,
        "confidence": 0.0,
        "prediction_time": record.created_at,
        "factors": []
    }