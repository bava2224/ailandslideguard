from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["Alerts"]
)


# ---------------------------------------------------------
# Enums
# ---------------------------------------------------------

class AlertLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


# ---------------------------------------------------------
# Request Schema
# ---------------------------------------------------------

class AlertCreate(BaseModel):
    location_id: Optional[str] = None

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    risk_score: float = Field(..., ge=0.0, le=1.0)

    level: AlertLevel

    title: str = Field(..., min_length=3, max_length=200)

    message: str = Field(..., min_length=3, max_length=1000)

    source: str = Field(
        default="risk_engine",
        max_length=100
    )


# ---------------------------------------------------------
# Response Schema
# ---------------------------------------------------------

class AlertResponse(BaseModel):
    id: int
    location_id: Optional[str]

    latitude: float
    longitude: float

    risk_score: float
    level: AlertLevel

    title: str
    message: str

    source: str

    status: AlertStatus

    created_at: datetime
    acknowledged_at: Optional[datetime] = None


# ---------------------------------------------------------
# Temporary storage
# ---------------------------------------------------------
# This is ONLY for protocol/demo development.
# Replace with PostgreSQL/PostGIS later.

alerts_db: list[AlertResponse] = []

next_alert_id = 1


# ---------------------------------------------------------
# Create Alert
# ---------------------------------------------------------

@router.post(
    "",
    response_model=AlertResponse,
    status_code=201
)
def create_alert(alert: AlertCreate):

    global next_alert_id

    new_alert = AlertResponse(
        id=next_alert_id,

        location_id=alert.location_id,

        latitude=alert.latitude,
        longitude=alert.longitude,

        risk_score=alert.risk_score,

        level=alert.level,

        title=alert.title,
        message=alert.message,

        source=alert.source,

        status=AlertStatus.ACTIVE,

        created_at=datetime.utcnow(),

        acknowledged_at=None
    )

    alerts_db.append(new_alert)

    next_alert_id += 1

    return new_alert


# ---------------------------------------------------------
# Get All Alerts
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[AlertResponse]
)
def get_alerts(
    status: Optional[AlertStatus] = Query(
        default=None
    ),

    level: Optional[AlertLevel] = Query(
        default=None
    )
):

    results = alerts_db

    if status:
        results = [
            alert
            for alert in results
            if alert.status == status
        ]

    if level:
        results = [
            alert
            for alert in results
            if alert.level == level
        ]

    return results


# ---------------------------------------------------------
# Get Single Alert
# ---------------------------------------------------------

@router.get(
    "/{alert_id}",
    response_model=AlertResponse
)
def get_alert(alert_id: int):

    for alert in alerts_db:

        if alert.id == alert_id:
            return alert

    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )


# ---------------------------------------------------------
# Acknowledge Alert
# ---------------------------------------------------------

@router.patch(
    "/{alert_id}/acknowledge",
    response_model=AlertResponse
)
def acknowledge_alert(alert_id: int):

    for index, alert in enumerate(alerts_db):

        if alert.id == alert_id:

            if alert.status == AlertStatus.RESOLVED:

                raise HTTPException(
                    status_code=400,
                    detail="Resolved alert cannot be acknowledged"
                )

            updated_alert = alert.model_copy(
                update={
                    "status": AlertStatus.ACKNOWLEDGED,
                    "acknowledged_at": datetime.utcnow()
                }
            )

            alerts_db[index] = updated_alert

            return updated_alert

    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )


# ---------------------------------------------------------
# Resolve Alert
# ---------------------------------------------------------

@router.patch(
    "/{alert_id}/resolve",
    response_model=AlertResponse
)
def resolve_alert(alert_id: int):

    for index, alert in enumerate(alerts_db):

        if alert.id == alert_id:

            updated_alert = alert.model_copy(
                update={
                    "status": AlertStatus.RESOLVED
                }
            )

            alerts_db[index] = updated_alert

            return updated_alert

    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )


# ---------------------------------------------------------
# Delete Alert
# ---------------------------------------------------------

@router.delete(
    "/{alert_id}"
)
def delete_alert(alert_id: int):

    for index, alert in enumerate(alerts_db):

        if alert.id == alert_id:

            alerts_db.pop(index)

            return {
                "message": "Alert deleted successfully",
                "alert_id": alert_id
            }

    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )