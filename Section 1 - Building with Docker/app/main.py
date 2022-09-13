import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel
from prophet import Prophet
import uvicorn

from app.core.config import Settings
from app.models.model import TempuratureModel


settings = Settings()

app = FastAPI()
model = TempuratureModel(f'{settings.DATA_DIR}/{settings.RALEIGH_TEMP_PATH}', settings.num_days, settings.date_column_name, settings.predict_col)

class PredictionRequest(BaseModel):
    prediction_window: int

@app.get('/ping')
def pong():
    return {'message': 'Pong!'}

@app.post('/predict')
def predict_tempuratures(request: PredictionRequest):
    data = request.dict()
    
    prediction_window = data['prediction_window']

    prediction = model.predict_temp(prediction_window)

    return {'forecast': prediction, 'window': prediction_window}