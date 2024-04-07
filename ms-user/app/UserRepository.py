import os

from app.models.UserUpdate import UserUpdate
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import UpdateResult

class UserRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def get_user_by_id(self, user_id: str) -> dict:
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def get_user_by_username(self, username: str) -> dict:
        return await self.collection.find_one({"username": username})

    async def get_user_by_email(self, email: str) -> dict:
        return await self.collection.find_one({"email": email})

    async def update_user_by_id(self, user_id: str, updated_user: UserUpdate) -> UpdateResult:
        updated_userdata = updated_user.model_dump(exclude_unset=True)
        updated_userdata["updated_at"] = datetime.now()
        return await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_userdata})

    async def delete_user_by_id(self, user_id: str) -> dict:
        return await self.collection.find_one_and_delete({"_id": ObjectId(user_id)})

    async def follow_user_by_id(self, user_id: str, follow_user_id: str) -> tuple[UpdateResult, UpdateResult]:
        query_following = {"$push": {"following": follow_user_id}}
        query_followers = {"$push": {"followers": user_id}}
        result_following = await self.collection.update_one({"_id": ObjectId(user_id)}, query_following)
        result_followers = await self.collection.update_one({"_id": ObjectId(follow_user_id)}, query_followers)
        return result_following, result_followers

    async def unfollow_user_by_id(self, user_id: str, unfollow_user_id: str) -> tuple[UpdateResult, UpdateResult]:
        query_following = {"$pull": {"following": unfollow_user_id}}
        query_followers = {"$pull": {"followers": user_id}}
        result_following = await self.collection.update_one({"_id": ObjectId(user_id)}, query_following)
        result_followers = await self.collection.update_one({"_id": ObjectId(unfollow_user_id)}, query_followers)
        return result_following, result_followers

    async def user_is_following_user(self, user_id: str, follow_user_id: str) -> bool:
        query = {
            "_id": ObjectId(user_id),
            "following": {"$elemMatch": {"$eq": follow_user_id}}
        }
        return bool(await self.collection.find(query).to_list(length=None))