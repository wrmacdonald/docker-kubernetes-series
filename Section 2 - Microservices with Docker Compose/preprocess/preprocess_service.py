from datetime import date
import pandas as pd
from pandas import DataFrame

from data_cleaner import DataCleaner


class PreproccessService:

    def __init__(self, city: str, date_column_name: str) -> None:
        """
            Args:
                temps_path (DataFrame): A Pandas DataFrame of monthly tempurature data.
                date_column_name (str): Name of a column containing date data (ex. `MyDateData`)

        """
        self.date_column_name = date_column_name
        self.pdtemps = pd.read_csv("../data/temperature_data_Raleigh_012020_062022.csv")

    def clean_data(self) -> DataFrame:
        """Prepare time series DataFrame for forecast"""
        temps_copy = DataCleaner(dataframe=self.pdtemps, date_column_name=self.date_column_name)
        temps_copy.convert_date()
        temps_copy.create_year_column()
        temps_copy.create_month_column()
        temps_copy.create_day_column()
        temps_copy.create_week_of_year_column()
        temps_copy.convert_to_numeric('TempMax', 'TempMin', 'TempAvg', verbose=True)
        temps_copy.drop_columns('TempDeparture', 'HDD', 'CDD', 'Precipitation', 'NewSnow', 'SnowDepth')

        return temps_copy