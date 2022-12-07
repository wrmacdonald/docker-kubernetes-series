from locale import D_FMT
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.core.models.database import engine
from app.core.schemas.request import PreprocessRequest
from app.core.models.models import RaleighTemps
from app.preprocess_service import PreproccessService


app = FastAPI(
    tite="Data Preprocessing API",
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

    city = data['city']

    preprocessor = PreproccessService(city=city)

    data_cleaned = preprocessor.clean_data()

    return {'forecast': data_cleaned}

@app.get('/temps/')
def read_temps():
    with Session(engine) as session:
        temps = session.exec(select(RaleighTemps)).all()
        return temps