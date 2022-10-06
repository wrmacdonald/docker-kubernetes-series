from sqlalchemy import Date

from sqlmodel import Field, SQLModel


class Tempuratures(SQLModel, table=True):
    __tablename__ = "raleigh_temps"

    measurementdate: str = Field(primary_key=True, unique=True)
    tempmax: float
    tempmin: float
    tempavg: float
    tempdeparture: float
    hdd: float
    cdd: float
    precipitation: str
    newsnow: str
    snowdepth: str