from functools import lru_cache

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core import config
from app.training.training_service import TrainingService
from app.core.schemas.schema import PredictionRequest


description = """
Temperature Forecast API let's you forecast for a timeframe of your choosing.

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

@app.get('/',
    summary='Predict API documentation redirect',
    description='Redirect to Predict API documentation',
    include_in_schema=False)
def predict_redirect_docs():
    return RedirectResponse("/docs/")

@app.post('/predict',
    summary="Get prediction",
    description="Get a forecast based on the window provided. Forecast will include a JSON representation of the DataFrame \
        as well as the window sent by request.",
        tags=["Main"])
def predict(request: PredictionRequest):
    data = request.dict()
    
    prediction_window, city = data['prediction_window'], (data['city'].lower())

    model = TrainingService(settings.test_window, city, settings.date_column_name, settings.predict_col)

    prediction = model.predict_temp(prediction_window)

    return {'forecast': prediction, 'window': prediction_window}