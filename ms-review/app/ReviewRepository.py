import os

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewCreateImage import ReviewCreateImage
from app.models.ReviewOut import ReviewOut
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import UpdateResult, InsertOneResult
from typing import List


class ReviewRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_review_db
        self.collection = db.review_collection


    async def add_review(self, review: ReviewCreate, user_id: str, username: str) -> InsertOneResult:
        review_dict = review.model_dump()
        review_dict["user_id"] = user_id
        review_dict["username"] = username
        return await self.collection.insert_one(review_dict)


    async def update_review_image(self, review_id: str, review_image: ReviewCreateImage) -> UpdateResult:
        updated_review = review_image.model_dump()
        return await self.collection.update_one({"_id": ObjectId(review_id)}, {"$set": updated_review})


    async def get_review_by_id(self, review_id: str) -> dict:
        return await self.collection.find_one({"_id": ObjectId(review_id)})

    async def get_feed_by_cursor_and_user_ids(self, timestamp_cursor: datetime, user_ids: List[str], page_size: int = 25) -> List[ReviewOut]:
        query = {
            "created_at": {"$lt": timestamp_cursor},
            "user_id": {"$in": user_ids}
        }
        return await self.collection.find(query).sort("created_at", -1).limit(page_size).to_list(length=page_size)


    async def get_reviews_by_user_id(self, user_id: str) -> List[ReviewOut]:
        return await self.collection.find({"user_id": user_id}).sort("created_at", -1).to_list(length=None)


    async def get_reviews_by_locations_and_usernames(self, location_ids: List[str], usernames: List[str]) -> List[ReviewOut]:
        query = {}
        if location_ids is not None:
            query["location.id"] = {"$in": location_ids}
        if usernames is not None:
            query["username"] = {"$in": usernames}
        return await self.collection.find(query).sort("created_at", -1).to_list(length=None)


    async def like_review_by_id(self, review_id: str, user_id: str) -> UpdateResult:
        query = {
            "$inc": {"like_count": 1},
            "$push": {"liked_by": user_id}
        }
        return await self.collection.update_one({"_id": ObjectId(review_id)}, query)


    async def unlike_review_by_id(self, review_id: str, user_id: str) -> UpdateResult:
        query = {
            "$inc": {"like_count": -1},
            "$pull": {"liked_by": user_id}
        }
        return await self.collection.update_one({"_id": ObjectId(review_id)}, query)


    async def user_has_liked_review(self, review_id: str, user_id: str) -> bool:
        query = {
            "_id": ObjectId(review_id),
            "liked_by": {"$elemMatch": {"$eq": user_id}}
        }
        return bool(await self.collection.find(query).to_list(length=None))