from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"]
)


# ---------------------------------------------------------
# Enums
# ---------------------------------------------------------

class ReportStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    VERIFIED = "VERIFIED"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


class ReportSeverity(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ---------------------------------------------------------
# Request
# ---------------------------------------------------------

class ReportCreate(BaseModel):

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    description: str = Field(
        ...,
        min_length=5,
        max_length=1000
    )

    severity: ReportSeverity

    photo_url: Optional[str] = None

    reporter_name: Optional[str] = None


# ---------------------------------------------------------
# Response
# ---------------------------------------------------------

class ReportResponse(BaseModel):

    id: int

    latitude: float
    longitude: float

    description: str

    severity: ReportSeverity

    photo_url: Optional[str]

    reporter_name: Optional[str]

    status: ReportStatus

    created_at: datetime

    verified_at: Optional[datetime] = None


# ---------------------------------------------------------
# Temporary storage
# ---------------------------------------------------------

reports_db: list[ReportResponse] = []

next_report_id = 1


# ---------------------------------------------------------
# Create report
# ---------------------------------------------------------

@router.post(
    "",
    response_model=ReportResponse,
    status_code=201
)
def create_report(report: ReportCreate):

    global next_report_id

    new_report = ReportResponse(

        id=next_report_id,

        latitude=report.latitude,
        longitude=report.longitude,

        description=report.description,

        severity=report.severity,

        photo_url=report.photo_url,

        reporter_name=report.reporter_name,

        status=ReportStatus.PENDING,

        created_at=datetime.utcnow(),

        verified_at=None
    )

    reports_db.append(new_report)

    next_report_id += 1

    return new_report


# ---------------------------------------------------------
# Get all reports
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[ReportResponse]
)
def get_reports():

    return reports_db


# ---------------------------------------------------------
# Get report
# ---------------------------------------------------------

@router.get(
    "/{report_id}",
    response_model=ReportResponse
)
def get_report(report_id: int):

    for report in reports_db:

        if report.id == report_id:
            return report

    raise HTTPException(
        status_code=404,
        detail="Report not found"
    )


# ---------------------------------------------------------
# Assign report
# ---------------------------------------------------------

@router.patch(
    "/{report_id}/assign",
    response_model=ReportResponse
)
def assign_report(report_id: int):

    for index, report in enumerate(reports_db):

        if report.id == report_id:

            updated = report.model_copy(
                update={
                    "status": ReportStatus.ASSIGNED
                }
            )

            reports_db[index] = updated

            return updated

    raise HTTPException(
        status_code=404,
        detail="Report not found"
    )


# ---------------------------------------------------------
# Verify report
# --------------------------------------------------------

@router.patch(
    "/{report_id}/verify",
    response_model=ReportResponse
)
def verify_report(
    report_id: int,
    confirmed: bool
):

    for index, report in enumerate(reports_db):

        if report.id == report_id:

            status = (
                ReportStatus.CONFIRMED
                if confirmed
                else ReportStatus.REJECTED
            )

            updated = report.model_copy(
                update={
                    "status": status,
                    "verified_at": datetime.utcnow()
                }
            )

            reports_db[index] = updated

            return updated

    raise HTTPException(
        status_code=404,
        detail="Report not found"
    )