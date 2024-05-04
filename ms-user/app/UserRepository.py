import os

from app.models.UserUpdate import UserUpdate
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import UpdateResult


class UserRepository:
    def __init__(self):
        """
        Initializes the UserRepository, setting up a MongoDB client and specifying the user collection.
        """
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_user_db
        self.collection = db.user_collection

    async def get_user_by_id(self, user_id: str) -> dict:
        """
        Retrieves a user's details by their ID.

        :param user_id: The ID of the user.
        :return: A dictionary containing the user's details or None if the user is not found.
        """
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def get_user_by_username(self, username: str) -> dict:
        """
        Retrieves a user's details by their name.

        :param username: The name of the user.
        :return: A dictionary containing the user's details or None if no user with that username exists.
        """
        return await self.collection.find_one({"username": username})

    async def get_user_by_email(self, email: str) -> dict:
        """
        Retrieves a user's details by their email address.

        :param email: The email address of the user.
        :return: A dictionary containing the user's details or None if no user with that email exists.
        """
        return await self.collection.find_one({"email": email})

    async def update_user_by_id(self, user_id: str, updated_user: UserUpdate) -> UpdateResult:
        """
        Updates the specified user's details in the database.

        :param user_id: The ID of the user to update.
        :param updated_user: The new details for the user (UserUpdate model).
        :return: The result of the update operation.
        """
        updated_userdata = updated_user.model_dump(exclude_unset=True)
        updated_userdata["updated_at"] = datetime.now()
        return await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_userdata})

    async def delete_user_by_id(self, user_id: str) -> dict:
        """
        Deletes a user's profile from the database by their ID.

        :param user_id: The ID of the user to be deleted.
        :return: The result of the delete operation.
        """
        return await self.collection.find_one_and_delete({"_id": ObjectId(user_id)})

    async def follow_user_by_id(self, user_id: str, follow_user_id: str) -> tuple[UpdateResult, UpdateResult]:
        """
        Allows a user to start following another user.

        :param user_id: The ID of the user who wants to follow another user.
        :param follow_user_id: The ID of the user to be followed.
        :return: A tuple containing the update results for both the following and followers updates.
        """
        query_following = {"$push": {"following": follow_user_id}}
        query_followers = {"$push": {"followers": user_id}}
        result_following = await self.collection.update_one({"_id": ObjectId(user_id)}, query_following)
        result_followers = await self.collection.update_one({"_id": ObjectId(follow_user_id)}, query_followers)
        return result_following, result_followers

    async def unfollow_user_by_id(self, user_id: str, unfollow_user_id: str) -> tuple[UpdateResult, UpdateResult]:
        """
        Allows a user to stop following another user.

        :param user_id: The ID of the user who wants to unfollow another user.
        :param unfollow_user_id: The ID of the user to be unfollowed.
        :return: A tuple containing the update results for both the following and followers updates.
        """
        query_following = {"$pull": {"following": unfollow_user_id}}
        query_followers = {"$pull": {"followers": user_id}}
        result_following = await self.collection.update_one({"_id": ObjectId(user_id)}, query_following)
        result_followers = await self.collection.update_one({"_id": ObjectId(unfollow_user_id)}, query_followers)
        return result_following, result_followers

    async def user_is_following_user(self, user_id: str, follow_user_id: str) -> bool:
        """
        Checks if a user is currently following another user.

        :param user_id: The ID of the user to check.
        :param follow_user_id: The ID of the user who might be followed.
        :return: True if the user is following the other user, otherwise False.
        """
        query = {
            "_id": ObjectId(user_id),
            "following": {"$elemMatch": {"$eq": follow_user_id}}
        }
        return bool(await self.collection.find(query).to_list(length=None))
