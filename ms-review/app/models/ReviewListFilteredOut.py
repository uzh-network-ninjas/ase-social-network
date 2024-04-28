from app.models.ReviewOut import ReviewOut
from pydantic import BaseModel
from typing import List


class LocationReviews(BaseModel):
    location_id: str
    average_rating: float
    reviews: List[ReviewOut]


class ReviewListFilteredOut(BaseModel):
    location_reviews: List[LocationReviews]