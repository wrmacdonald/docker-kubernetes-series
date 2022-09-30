from sqlalchemy import Column, Date, Float, String

from app.core.models.database import Base


class Tempurature(Base):
    __tablename__ = "tempuratures"

    measurement_date = Column(Date, primary_key=True, unique=True, index=True)
    temp_max = Column(Float)
    temp_min = Column(Float)
    temp_avg = Column(Float)
    temp_departure = Column(Float)
    hdd = Column(Float)
    cdd = Column(Float)
    precipitation = Column(String)
    new_snow = Column(String)
    snow_depth = Column(String)