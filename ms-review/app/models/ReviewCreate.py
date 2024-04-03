from datetime import datetime
from Location import Location
from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    text: str
    rating: int
    image: Optional[str] = None
    location: Location
    created_at: Optional[datetime] = datetime.now()