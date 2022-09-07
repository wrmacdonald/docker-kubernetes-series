from fastapi import FastAPI
from pydantic import BaseModel
from prophet import Prophet
import uvicorn

from model import TempuratureModel

app = FastAPI()
model = TempuratureModel()

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
    uvicorn.run('predict:app', host='127.0.0.1', port=8000, reload=True)
    