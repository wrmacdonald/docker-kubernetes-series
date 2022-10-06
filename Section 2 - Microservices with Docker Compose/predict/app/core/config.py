import os

from pydantic import BaseSettings

class Settings(BaseSettings):

    test_window: int = 30
    date_column_name: str ='measurementdate'
    predict_col: str ='tempmax'
    DATA_DIR: str = os.path.join(os.path.abspath(os.getcwd()), 'data')
    RALEIGH_TEMP_PATH: str

    class Config:
        env_file = "app/.env"