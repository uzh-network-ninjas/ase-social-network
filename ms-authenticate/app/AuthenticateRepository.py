from datetime import datetime
import os
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.UserRegister import UserRegister
from app.models.UserLogin import UserLogin


class AuthenticateRepository:
    def __init__(self):
        """
        Initializes the AuthenticateRepository with a MongoDB client, connecting to the specified database and collection
        for user data.
        """
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def user_exists(self, user: UserLogin) -> bool:
        """
        Checks if a user exists in the database either by username or email.

        :param user: The user data (UserLogin model).
        :return: True if the user exists, False otherwise.
        """
        if await self.collection.find_one({
            '$or': [
                {'username': user.username},
                {'email': user.email}
            ]
        }):
            return True
        return False

    async def username_exists(self, username: str) -> bool:
        """
        Checks if a username exists in the database.

        :param username: The username to check.
        :return: True if the username exists, False otherwise.
        """
        if await self.collection.find_one({"username": username}):
            return True
        return False

    async def user_email_exists(self, email: str) -> bool:
        """
        Checks if an email is already registered in the database.

        :param email: The email to check.
        :return: True if the email exists, False otherwise.
        """
        if await self.collection.find_one({"email": email}):
            return True
        return False

    async def add_user(self, user: UserRegister) -> UserLogin:
        """
        Registers a new user in the database.

        :param user: The user registration data (UserRegister model).
        :return: A UserLogin object representing the registered user.
        """
        user_dict = user.model_dump()
        user_dict["created_at"] = datetime.now()
        result = await self.collection.insert_one(user_dict)
        user_dict['id'] = str(result.inserted_id)
        return UserLogin(**user_dict)

    async def get_user_by_name_or_email(self, user: UserLogin) -> UserLogin:
        """
        Retrieves a user's details from the database by username or email.

        :param user: The user login information.
        :return: A UserLogin object representing the found user.
        """
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
        """
        Retrieves a user's details from the database by their ID.

        :param user_id: The ID of the user.
        :return: A UserLogin object representing the found user.
        """
        result = await self.collection.find_one({"_id": ObjectId(user_id)})
        found_user = UserLogin(**result)
        found_user.id = str(result["_id"])
        return found_user

    async def update_user_password(self, user_id: str, new_password: str):
        """
        Updates a user's password.

        :param user_id: The user's ID.
        :param new_password: The new password to set.
        """
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                'password': new_password,
                'updated_at': datetime.now()
            }}
        )
