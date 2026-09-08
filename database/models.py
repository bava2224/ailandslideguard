from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class LandslideData(Base):
    __tablename__ = "landslide_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    soil_moisture = Column(Float, nullable=True)
    risk_level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)