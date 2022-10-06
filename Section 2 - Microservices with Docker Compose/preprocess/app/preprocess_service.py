

from sqlmodel import select, Session
import pandas as pd
from pandas import DataFrame

from app.data_cleaner import DataCleaner
from app.core.models.database import engine
from app.core.models.models import Tempuratures


class PreproccessService:
    """Prepares a dataframe for time series forecasting model.

        Retrieves data from PostgreSQL database and creates a Pandas dataframe. The data from that dataframe
        is cleaned and the clean dataframe is returned to the caller.
    """

    def __init__(self, city: str = 'raleigh', date_column_name: str = 'measurementdate') -> None:
        """
            Args:
                city (str): City to retrieve and process data for.
                date_column_name (str): Name of a column containing date data (ex. `MyDateData`)

        """
        self._city = city
        self._date_column_name = date_column_name
        #self._pdtemps = pd.read_csv("../../data/temperature_data_Raleigh_012020_062022.csv")
        self._pdtemps = self._read_temps()
        print

    def _read_temps(self):
        with Session(engine) as session:
            temps = session.exec(select(Tempuratures)).all()
        df = pd.DataFrame([vars(t) for t in temps])
        return df
            

    def clean_data(self) -> DataFrame:
        """Clean time series DataFrame for forecast"""
        temps_copy = DataCleaner(dataframe=self._pdtemps, date_column_name=self._date_column_name)
        temps_copy.convert_date()
        temps_copy.create_year_column()
        temps_copy.create_month_column()
        temps_copy.create_day_column()
        temps_copy.create_week_of_year_column()
        temps_copy.convert_to_numeric('tempmax', 'tempmin', 'tempavg', verbose=True)
        temps_copy.drop_columns('_sa_instance_state', 'tempdeparture', 'hdd', 'cdd', 'precipitation', 'newsnow', 'snowdepth')
        trainDF = temps_copy.dataframe.sort_values(by=self._date_column_name).iloc[0:-30]
        print(trainDF[:10])

        return trainDF.to_json(orient='index', date_format='iso')