from pydantic import BaseModel
from typing import Optional


class ReviewOut(BaseModel):
    user_id: str #TODO return username that gets fetched from ms-user too, right?
    id: str
    text: str
    rating: int
    image: Optional[str] = None
    location: str