from datetime import date
import pandas as pd
from pandas import DataFrame

from app.data_cleaner import DataCleaner


class PreproccessService:
    """Prepares a dataframe for time series forecasting model.

        Retrieves data from PostgreSQL database and creates a Pandas dataframe. The data from that dataframe
        is cleaned and the clean dataframe is returned to the caller.
    """

    def __init__(self, city: str = 'raleigh', date_column_name: str = 'MeasurementDate') -> None:
        """
            Args:
                city (str): City to retrieve and process data for.
                date_column_name (str): Name of a column containing date data (ex. `MyDateData`)

        """
        self.date_column_name = date_column_name
        self.pdtemps = pd.read_csv("../../data/temperature_data_Raleigh_012020_062022.csv")

    def clean_data(self) -> DataFrame:
        """Clean time series DataFrame for forecast"""
        temps_copy = DataCleaner(dataframe=self.pdtemps, date_column_name=self.date_column_name)
        temps_copy.convert_date()
        temps_copy.create_year_column()
        temps_copy.create_month_column()
        temps_copy.create_day_column()
        temps_copy.create_week_of_year_column()
        temps_copy.convert_to_numeric('TempMax', 'TempMin', 'TempAvg', verbose=True)
        temps_copy.drop_columns('TempDeparture', 'HDD', 'CDD', 'Precipitation', 'NewSnow', 'SnowDepth')

        trainDF = temps_copy.dataframe.sort_values(by=self.date_column_name).iloc[0:-30]

        return trainDF.to_json(orient='index', date_format='iso')