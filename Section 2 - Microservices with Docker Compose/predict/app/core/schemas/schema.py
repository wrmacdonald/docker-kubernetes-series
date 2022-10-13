from pydantic import BaseModel


class PredictionRequest(BaseModel):
    prediction_window: int
    city: str

