from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    user_id: Optional[str] = None
    text: str
    rating: int
    image: Optional[str] = None
    location: str
    created_at: Optional[datetime] = datetime.now()

class ReviewCreateImage(BaseModel):
    image: str

class ReviewOut(BaseModel):
    user_id: str #TODO return username that gets fetched from ms-user too, right?
    id: str
    text: str
    rating: int
    image: Optional[str] = None
    location: str