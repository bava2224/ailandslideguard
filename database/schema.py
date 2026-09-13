# database/schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LandslideDataBase(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rainfall: Optional[float] = None
    soil_moisture: Optional[float] = None
    risk_level: str

class LandslideDataCreate(LandslideDataBase):
    pass

class LandslideDataResponse(LandslideDataBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True