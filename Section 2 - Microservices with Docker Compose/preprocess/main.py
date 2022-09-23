from locale import D_FMT
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.schemas.request import PreprocessRequest
from preprocess_service import PreproccessService

description = """
Data Preprocessing API allows for preprocessing temperature time series data
for training the forecasting model.

## /

Redirect to Tempurature Forecast API docs.

## Preprocess

Prepare data for training tempurature forecast model 
"""

app = FastAPI(
    tite="Data Preprocessing API",
    description=description,
    version="0.1.0"
)

@app.get('/',
    summary='API documentation redirect',
    description='Redirect to API documentation at /docs/')
def main():
    return RedirectResponse("/docs/")

@app.post('/preprocess',
    summary="Preprocess data",
    description="Prepare data for temperature forecast model training.")
def preprocess(request: PreprocessRequest):
    data = request.dict()

    df = data['city']

    preprocessor = PreproccessService(df, 'MeasurementDate')

    data_cleaned = preprocessor.clean_data()

    return {'data': data_cleaned}