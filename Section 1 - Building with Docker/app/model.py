import pandas as pd
from pandas import DataFrame
from prophet import Prophet

from data_cleaner import DataCleaner



class TempuratureModel:
    """Creates instance of tempurature forecasting model

        Creates a model that will forecast tempurature data for a specified number of days.
        It defaults to Raleigh but can accept any arbitrary monthly tempurature data which can be downloaded
        from https://www.weather.gov/wrh/climate.

        Attributes:
            _model (Prophet): A trained Prophet time-series forecasting model. 
    """

    def __init__(self, num_days=30, date_column_name: str='MeasurementDate', predict_col: str='TempMax', predict_window: int=30) -> None:
        """
            Args:
                pdtemps (DataFrame): A Pandas DataFrame of monthly tempurature data.
                num_days (int): Number of days to filter out for test data.
                date_column_name (str): Name of a column containing date data (ex. `MyDateData`)
                predict_col (str): Column of data to be predicted.
                predict_window (int):
        """

        self.pdtemps = pd.read_csv('../data/temperature_data_Raleigh_012020_062022.csv')
        self.num_days = num_days
        self.date_column_name = date_column_name
        self.predict_col = predict_col
        self.predict_window = predict_window

        self._model = self._train_model()
            
    def _clean_data(self) -> DataFrame:
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


    def _train_model(self, growth: str='flat', daily_seasonality: bool=False, weekly_seasonality: bool=True, yearly_seasonality: bool=True):
        """Train a Prophet model with cleaned data
        
            Args:
                growth (str): Type of growth trend the use for time series modeling.
                daily_seasonality (bool): Whether to take in to account daily seasonlity for model.
                weekly_seasonality (bool): Whether to take into account weekly seasonality for model.
                yearly_seasonality (bool): Whether to take into account yearly seasonlity for model.
        """
        clean_data = self._clean_data()
        trainDF = clean_data.dataframe.sort_values(by=self.date_column_name).iloc[0:-self.num_days]

        prophetDF = pd.DataFrame()
        prophetDF['ds'] = trainDF[self.date_column_name]
        prophetDF['y'] = trainDF[self.predict_col]

        m = Prophet(growth=growth, 
              daily_seasonality=daily_seasonality, 
              weekly_seasonality=weekly_seasonality,
              yearly_seasonality=yearly_seasonality
             )

        prophet_time_series_model = m.fit(prophetDF)
        
        return prophet_time_series_model

    def predict_temp(self, prediction_window: int=30) -> DataFrame:
        """Forecast tempuratures for N days.
        
            Args:
                predictions_window (int): Number of days to forecast.
        """
        futureDF = self._model.make_future_dataframe(periods=prediction_window)
        forecastDF = self._model.predict(futureDF)

        return forecastDF


