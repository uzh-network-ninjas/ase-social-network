import os

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewOut import ReviewOut
from app.models.ReviewCreateImage import ReviewCreateImage
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import UpdateResult, InsertOneResult


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