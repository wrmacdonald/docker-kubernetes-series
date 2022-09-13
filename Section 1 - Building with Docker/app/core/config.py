import os

from pydantic import BaseSettings

class Settings(BaseSettings):

    num_days: int = 30
    date_column_name: str ='MeasurementDate'
    predict_col: str ='TempMax'
    DATA_DIR: str = os.path.join(os.path.abspath(os.getcwd()), 'data')
    RALEIGH_TEMP_PATH: str

    class Config:
        env_file = "app/.env"