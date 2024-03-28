import os

from app.models.Review import ReviewCreate, ReviewOut
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

class ReviewRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_review_db
        self.collection = db.review_collection

    async def add_review(self, review: ReviewCreate) -> ReviewOut:
        raise NotImplementedError

    async def add_review_image(self, review: ReviewCreate) -> ReviewOut:
        raise NotImplementedError

    async def get_review_by_id(self, review_id: str) -> dict:
        raise await self.collection.find_one({"_id": ObjectId(review_id)})