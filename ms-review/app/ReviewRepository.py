import os

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewCreateImage import ReviewCreateImage
from app.models.ReviewOut import ReviewOut
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCursor
from pymongo.results import UpdateResult, InsertOneResult
from typing import List


class ReviewRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_review_db
        self.collection = db.review_collection

    async def add_review(self, user_id: str, review: ReviewCreate) -> InsertOneResult:
        review_dict = review.model_dump()
        review_dict["user_id"] = user_id
        return await self.collection.insert_one(review_dict)

    async def update_review_image(self, review_id: str, review_image: ReviewCreateImage) -> UpdateResult:
        updated_review = review_image.model_dump()
        return await self.collection.update_one({"_id": ObjectId(review_id)}, {"$set": updated_review})

    async def get_review_by_id(self, review_id: str) -> dict:
        return await self.collection.find_one({"_id": ObjectId(review_id)})

    async def get_feed_by_cursor_and_user_ids(self, timestamp_cursor: datetime, user_ids: List[str], page_size=25) -> List[ReviewOut]:
        query = {
            "created_at": {"$lt": timestamp_cursor},
            "user_id": {"$in": user_ids}
        }
        cursor = self.collection.find(query).sort("created_at", -1).limit(page_size)
        return await cursor.to_list(length=page_size)
