from functools import lru_cache

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core import config
from app.training.model_trainer import ModelTrainingService
from app.core.schemas.schema import PredictionRequest


description = """
Temperature Forecast API let's you forecast for a timeframe of your choosing.

## Predict/Docs

Redirect to Tempurature Forecast API docs.

## Predict 

Get prediction for specified time window and testing.
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

model = ModelTrainingService(f'{settings.DATA_DIR}/{settings.RALEIGH_TEMP_PATH}', settings.num_days, settings.date_column_name, settings.predict_col)

@app.get('/predict/docs',
    summary='API documentation redirect',
    description='Redirect to Temperature Forecast API documentation at /docs/')
def main():
    return RedirectResponse("/docs/")

@app.get('/preprocess/docs',
    summary='API documentation redirect',
    description='Redirect to Data Preprocess API documentation ')
def main():
    return RedirectResponse("http://preprocess:8000/docs/")

@app.post('/predict',
    summary="Get prediction",
    description="Get a forecast based on the window provided. Forecast will include a JSON representation of the DataFrame \
        as well as the window sent by request.")
def predict(request: PredictionRequest):
    data = request.dict()
    
    prediction_window = data['prediction_window']

    prediction = model.predict_temp(prediction_window)

    return {'forecast': prediction, 'window': prediction_window}