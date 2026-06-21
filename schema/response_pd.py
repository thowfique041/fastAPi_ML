from pydantic import BaseModel
from typing import Dict

class Prediction(BaseModel):
    prediction: str
    probability: Dict[str, float]

class PredictionResponse(BaseModel):
    name: str
    prediction: Prediction