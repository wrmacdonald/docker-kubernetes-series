from functools import lru_cache
import socket

from fastapi import FastAPI
from pydantic import BaseModel

from app.core import config
from app.models.model import TempuratureModel

description = """
Temperature Forecast API let's you forecast for a timeframe of your choosing.

## Hostname

Get hostname of host running API.

## Predict 

Get prediction for specified time window.
"""

@lru_cache()
def get_settings():
    return config.Settings()

settings = get_settings()

app = FastAPI(
    title="Tempurature Forecast API",
    description=description,
    version="0.1.0"
    )

model = TempuratureModel(f'{settings.DATA_DIR}/{settings.RALEIGH_TEMP_PATH}', settings.num_days, settings.date_column_name, settings.predict_col)

class PredictionRequest(BaseModel):
    prediction_window: int

@app.get('/hostname',
    summary='Demo',
    description='Get hostname of host running API.')
def pong():
    hostname = socket.gethostname()
    return {'hostname': hostname}

@app.post('/predict',
    summary="Get prediction",
    description="Get a forecast based on the window provided. Forecast will include a JSON representation of the DataFrame \
        as well as the window sent by request.")

def predict_tempuratures(request: PredictionRequest):
    data = request.dict()
    
    prediction_window = data['prediction_window']

    prediction = model.predict_temp(prediction_window)

    return {'forecast': prediction, 'window': prediction_window}