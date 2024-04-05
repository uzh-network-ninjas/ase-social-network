from app.models.ReviewOut import ReviewOut
from pydantic import BaseModel
from typing import List


class ReviewListOut(BaseModel):
    reviews: List[ReviewOut]