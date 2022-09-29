from typing import Any

from pydantic import BaseModel


class PreprocessRequest(BaseModel):
    prediction_window: int