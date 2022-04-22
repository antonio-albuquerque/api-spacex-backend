from datetime import datetime
from pydantic import BaseModel, validator


class Satelite(BaseModel):
    id: int
    latitude: float
    longitude: float
    creation_date: datetime
    satelite_id: str
    message: str


class NearestSatelite(Satelite):
    distance: float
    unit: str
