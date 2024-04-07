from app.models.Location import Location
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class ReviewCreate(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    text: str
    rating: int
    image: Optional[str] = None
    location: Location
    like_count: Optional[int] = 0
    liked_by: Optional[List[str]] = []
    created_at: Optional[datetime] = None