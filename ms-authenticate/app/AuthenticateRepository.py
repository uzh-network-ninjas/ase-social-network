import os

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models.User import User


class AuthenticateRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def user_exists(self, user_id: str):
        result = await self.collection.find_one({"_id": ObjectId(user_id)})
        if result:
            return True
        return False

    async def add_user(self, user: User):
        user_dict = user.model_dump()
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_user(self, user_id: str):
        result = await self.collection.find_one({"_id": ObjectId(user_id)})
        result["id"] = str(result["_id"])
        return User(**result)

    async def delete_user(self, user_id: str):
        _ = await self.collection.find_one_and_delete({"_id": ObjectId(user_id)})
