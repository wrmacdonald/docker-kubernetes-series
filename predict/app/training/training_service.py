import json
import requests

import pandas as pd
from pandas import DataFrame
from prophet import Prophet


class TrainingService:
    """Creates instance of tempurature forecasting model

        Creates a model that will forecast tempurature data for a specified number of days.
        It defaults to Raleigh but can accept any arbitrary monthly tempurature data which can be downloaded
        from https://www.weather.gov/wrh/climate.

        Attributes:
            _model (Prophet): A trained Prophet time-series forecasting model. 
    """

    def __init__(self, test_window: int, city: str, date_column_name: str, predict_col: str) -> None:
        """
            Args:
                num_days (int): Number of days to filter out for test data.
                city (str): City to predict temp for.f
                date_column_name (str): Name of a column containing date data (ex. `MyDateData`)
                predict_col (str): Column of data to be predicted.
        """

        self._city = city
        self._test_window = test_window
        self._date_column_name = date_column_name
        self._predict_col = predict_col
        self._preprocess_endpoint = "http://preprocess:8000/preprocess"

        self._model = self._train_model()

    def _preprocess_data(self) -> DataFrame:
        """
            Make request to preprocess service for training data.
        """
        request_obj = {"test_window": self._test_window, "city": self._city}
        r = requests.post(self._preprocess_endpoint, json=request_obj)
        return r.json()


    def _train_model(self, growth: str='flat', daily_seasonality: bool=False, weekly_seasonality: bool=True, yearly_seasonality: bool=True):
        """Train a Prophet model with cleaned data
        
            Args:
                growth (str): Type of growth trend the use for time series modeling.
                daily_seasonality (bool): Whether to take in to account daily seasonlity for model.
                weekly_seasonality (bool): Whether to take into account weekly seasonality for model.
                yearly_seasonality (bool): Whether to take into account yearly seasonlity for model.
        """
        train_data = self._preprocess_data()
        train_df = pd.read_json(train_data['forecast'], orient='index')

        prophetDF = pd.DataFrame()
        prophetDF['ds'] = train_df[self._date_column_name]
        prophetDF['y'] = train_df[self._predict_col]

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