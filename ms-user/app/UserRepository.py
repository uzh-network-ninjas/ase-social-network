import os

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.User import UserOut, UserUpdate

class UserRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def find_by_id(self, user_id: str):
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def find_by_username(self, username: str):
        return await self.collection.find_one({"username": username})

    async def update_user(self, user_id: str, updated_user: UserUpdate):
        updated_userdata = updated_user.model_dump(exclude_unset=True)
        return await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_userdata})

    async def delete_user_by_id(self, user_id: str):
        return await self.collection.find_one_and_delete({"_id": ObjectId(user_id)})