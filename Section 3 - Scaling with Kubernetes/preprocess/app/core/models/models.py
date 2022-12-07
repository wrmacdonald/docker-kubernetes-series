from sqlalchemy import Date

from sqlmodel import Field, SQLModel


class RaleighTemps(SQLModel, table=True):
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

class PortlandTemps(SQLModel, table=True):
    __tablename__ = "portland_temps"

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

tempuratures = {"raleigh": RaleighTemps,
                "portland": PortlandTemps
}