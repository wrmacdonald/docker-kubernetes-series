from pydantic import BaseModel


class PreprocessRequest(BaseModel):
    city: str