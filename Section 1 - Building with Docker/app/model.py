import pandas as pd
from pandas import DataFrame
from prophet import Prophet
import spark

from data_utils import DataCleaner

class TempuratureModel:

    def __init__(self, num_days=30, date_column_name: str='MeasurementDate', predict_col: str='TempMax', predict_window: int=30) -> None:
        self.pdtemps = spark.read.option("header",True).csv('../data/temperature_data_Raleigh_012020_062022.csv').toPandas()
        self.num_days = num_days
        self.data_column_name = date_column_name
        self.predict_col = predict_col
        self.predict_window = predict_window

        self.model = self._train_model()

    def _train_model(self, growth: str='flat', daily_seasonality: bool=False, weekly_seasonality: bool=True, yearly_seasonality: bool=True):
        clean_data = self._clean_data()
        trainDF = clean_data.sort_values(by=self.data_column_name).iloc[0:-self.num_days]

        prophetDF = pd.DataFrame()
        prophetDF['ds'] = trainDF[self.data_column_name]
        prophetDF['y'] = trainDF[self.predict_col]

        m = Prophet(growth=growth, 
              daily_seasonality=daily_seasonality, 
              weekly_seasonality=weekly_seasonality,
              yearly_seasonality=yearly_seasonality
             )

        prophet_time_series_model = m.fit(prophetDF)
        
        return prophet_time_series_model
            
    def _clean_data(self) -> DataFrame:
        temps_copy = self.pdtemps.copy()
        temps_copy = DataCleaner(dataframe=temps_copy, date_column_name=self.date_column_name)
        temps_copy.convert_date()
        temps_copy.create_year_column()
        temps_copy.create_month_column()
        temps_copy.create_day_column()
        temps_copy.create_week_of_year_column()
        temps_copy.convert_to_numeric('TempMax', 'TempMin', 'TempAvg', verbose=True)
        temps_copy.drop_columns(['TempDeparture', 'HDD', 'CDD', 'Precipitation', 'NewSnow', 'SnowDepth'])

        return temps_copy


    def predict_temp(self, prediction_window: int=30) -> DataFrame:
        
        futureDF = self.model.make_future_dataframe(periods=prediction_window)
        forecastDF = self.model.predict(futureDF)

        return forecastDF


