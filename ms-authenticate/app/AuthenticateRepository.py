import os
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.UserIn import UserIn


class AuthenticateRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def find_user(self, user: UserIn):
        if await self.collection.find_one({
            '$or': [
                {'username': user.username},
                {'email': user.email}
            ]
        }):
            return True
        return False

    async def find_user_by_name(self, username: str):
        if await self.collection.find_one({"username": username}):
            return True
        return False

    async def find_user_by_email(self, email: str):
        if await self.collection.find_one({"email": email}):
            return True
        return False

    async def add_user(self, user: UserIn):
        user_dict = user.model_dump()
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_user(self, user: UserIn):
        result = await self.collection.find_one({
            '$or': [
                {'username': user.username},
                {'email': user.email}
            ]
        })
        return UserIn(**result)
