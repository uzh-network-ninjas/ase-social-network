import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.UserRegisterIn import UserRegisterIn
from app.models.UserLoginIn import UserLoginIn
from app.models.UserOut import UserOut


class AuthenticateRepository:
    def __init__(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def user_exists(self, user: UserLoginIn) -> bool:
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

    async def add_user(self, user: UserRegisterIn) -> UserOut:
        user_dict = user.model_dump()
        result = await self.collection.insert_one(user_dict)
        user_dict['id'] = str(result.inserted_id)
        return UserOut(**user_dict)

    async def get_user_by_name_or_email(self, user: UserLoginIn) -> UserLoginIn:
        result = await self.collection.find_one({
            '$or': [
                {'username': user.username},
                {'email': user.email}
            ]
        })
        found_user = UserLoginIn(**result)
        found_user.id = str(result["_id"])
        return found_user