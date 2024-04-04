from pydantic import BaseModel


class Coordinates(BaseModel):
    x: float
    y: float


class Location(BaseModel):
    id: str
    name: str
    coordinates: Coordinates