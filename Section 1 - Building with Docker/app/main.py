import os

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from prophet import Prophet
import uvicorn

from core.config import Settings
from model import TempuratureModel


settings = Settings()

app = FastAPI()
model = TempuratureModel(f'{settings.DATA_DIR}/{settings.RALEIGH_TEMP_PATH}', settings.num_days, settings.date_column_name, settings.predict_col)

class PredictionRequest(BaseModel):
    prediction_window: int

@app.get('/ping')
async def pong():
    return {'message': 'Pong!'}

@app.post('/predict')
def predict_tempuratures(request: PredictionRequest):
    data = request.dict()
    
    prediction_window = data['prediction_window']

    prediction = model.predict_temp(data['prediction_window'])

    return {'forecast': prediction, 'window': prediction_window}

if __name__ == '__main__':
    uvicorn.run('main:app', host=os.getenv('HOST', '127.0.0.1'), port=os.getenv('PORT', 8000), reload=True)