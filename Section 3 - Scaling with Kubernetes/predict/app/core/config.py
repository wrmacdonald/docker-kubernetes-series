import os

from pydantic import BaseSettings

class Settings(BaseSettings):

    test_window: int = 30
    date_column_name: str ='measurementdate'
    predict_col: str ='tempmax'