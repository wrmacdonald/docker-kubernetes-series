from sqlalchemy import Column, Date, Float, Integer

from app.core.models.database import Base


class Tempurature(Base):
    __tablename__ = "tempuratures"

    measurement_date = Column(Date, primary_key=True, unique=True, index=True)
    temp_max = Column(Integer)
    temp_min = Column(Integer)
    temp_avg = Column(Float)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    week_of_year = Column(Integer)


