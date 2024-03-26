from datetime import datetime
import os
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.UserRegister import UserRegister
from app.models.UserLogin import UserLogin
from app.models.UserOut import UserOut


class AuthenticateRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def user_exists(self, user: UserLogin) -> bool:
        if await self.collection.find_one({
            '$or': [
                {'username': user.username},
                {'email': user.email}
            ]
        }):
            return True
        return False

    async def username_exists(self, username: str) -> bool:
        if await self.collection.find_one({"username": username}):
            return True
        return False

    async def user_email_exists(self, email: str) -> bool:
        if await self.collection.find_one({"email": email}):
            return True
        return False

    async def add_user(self, user: UserRegister) -> UserOut:
        user_dict = user.model_dump()
        result = await self.collection.insert_one(user_dict)
        user_dict['id'] = str(result.inserted_id)
        return UserOut(**user_dict)

    async def get_user_by_name_or_email(self, user: UserLogin) -> UserLogin:
        result = await self.collection.find_one({
            '$or': [
                {'username': user.username},
                {'email': user.email}
            ]
        })
        found_user = UserLogin(**result)
        found_user.id = str(result["_id"])
        return found_user

    async def get_user_by_id(self, user_id: str) -> UserLogin:
        result = await self.collection.find_one({"_id": ObjectId(user_id)})
        found_user = UserLogin(**result)
        found_user.id = str(result["_id"])
        return found_user

    async def update_user_password(self, user_id: str, new_password: str):
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                'password': new_password,
                'updated_at': datetime.now()
            }}
        )
