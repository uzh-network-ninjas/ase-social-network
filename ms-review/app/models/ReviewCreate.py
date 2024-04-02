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