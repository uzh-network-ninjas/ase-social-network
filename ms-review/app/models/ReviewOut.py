from app.models.Location import Location
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReviewOut(BaseModel):
    id: str
    user_id: str
    username: str
    text: str
    rating: int
    image: Optional[str] = None
    location: Location
    like_count: int
    liked_by_current_user: bool
    created_at: datetime