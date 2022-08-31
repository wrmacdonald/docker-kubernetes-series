from fastapi import FastAPI
from prophet import Prophet


app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello, World!'}