import boto3
import jwt
import os

from bson import ObjectId
from app.models.DietaryCriteria import DietaryCriteria
from app.models.Preferences import Preferences
from app.models.Restrictions import Restrictions
from app.models.UserUpdate import UserUpdate
from app.models.UserOut import UserOut
from app.models.UserListOut import UserListOut
from app.UserRepository import UserRepository
from app.logging_config import logger
from fastapi import HTTPException, Request, UploadFile


class UserService:
    def __init__(self):
        """
        Initializes the UserService with a UserRepository to interact with user data stored in a database.
        """
        self.user_repo = UserRepository()

    async def get_user_by_id(self, user_id: str) -> UserOut:
        """
        Retrieves a user's detailed information by their ID.

        :param user_id: The ID of the user.
        :return: A UserOut object containing the user's detailed information.
        :raises HTTPException(404): If the user is not found in the database.
        """
        result = await self.user_repo.get_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    async def get_user_by_username(self, username: str) -> UserOut:
        """
        Retrieves a user's detailed information by their name.

        :param username: The name of the user.
        :return: A UserOut object containing the user's detailed information.
        :raises HTTPException(404): If no user with the specified name is found.
        """
        result = await self.user_repo.get_user_by_username(username)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    async def update_user_by_id(self, user_id: str, updated_user: UserUpdate) -> UserOut:
        """
        Updates a user's profile based on the provided information.

        :param user_id: The ID of the user to be updated.
        :param updated_user: The updated user data (UserUpdate model).
        :return: A UserOut object showing the updated user details.
        :raises HTTPException(404): If the user is not found
        :raises HTTPException(400): If username/email is taken
        :raises HTTPException(404): If provided preferences/restrictions are invalid.
        """
        if not await self.user_repo.get_user_by_id(user_id):
            raise HTTPException(status_code=404, detail="User not found!")
        username = await self.user_repo.get_user_by_username(updated_user.username)
        email = await self.user_repo.get_user_by_email(updated_user.email)
        detail = (f"Username already taken: {updated_user.username}!" if username else "") \
                 + (" " if username and email else "") \
                 + (f"Email already taken: {updated_user.email}!" if email else "")
        if detail:
            raise HTTPException(status_code=400, detail=detail)
        preferences = [preference for preference in updated_user.preferences if preference not in Preferences]
        restrictions = [restriction for restriction in updated_user.restrictions if restriction not in Restrictions]
        if preferences or restrictions:
            raise HTTPException(status_code=400, detail=f"Preferences/Restrictions do not exist: "
                                                        f"{', '.join(preferences + restrictions)}")
        result = await self.user_repo.update_user_by_id(user_id, updated_user)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update user details!")
        return await self.get_user_by_id(user_id)

    async def update_user_image_by_id(self, user_id: str, image: UploadFile) -> UserOut:
        """
        Updates the profile image of a user.

        :param user_id: The ID of the user.
        :param image: The image file to upload.
        :return: A UserOut object showing the updated user details.
        :raises HTTPException(404): If the user is not found.
        :raises HTTPException(400): If the image could not be uploaded to s3.
        :raises HTTPException(400): If the database could not update the image reference.
        """
        if not await self.user_repo.get_user_by_id(user_id):
            raise HTTPException(status_code=404, detail="User not found!")
        bucket_name = "ms-user"
        s3_folder = "user-images"
        s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )

        try:
            file_content = await image.read()
            object_key = f"{s3_folder}/{user_id}/{image.filename}"
            s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
        except Exception as e:
            logger.error(f"Could not upload an image to s3: {e}")
            raise HTTPException(status_code=400, detail="Could not update user profile picture!")

        updated_user = UserUpdate(image=f"{os.getenv("S3_DEFAULT_INSTANCE", "http://localhost:4566")}/{bucket_name}/{object_key}")
        return await self.update_user_by_id(user_id, updated_user)

    async def delete_user_by_id(self, user_id: str):
        """
        Deletes a user's profile from the database.

        :param user_id: The ID of the user to be deleted.
        :raises HTTPException(404): If the user is not found.
        """
        result = await self.user_repo.delete_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")

    async def follow_user_by_id(self, user_id: str, follow_user_id: str) -> UserOut:
        """
        Enables one user to start following another by updating their following list.

        :param user_id: The ID of the user who wants to follow another user.
        :param follow_user_id: The ID of the user to be followed.
        :return: A UserOut object showing the updated details of the following user.
        :raises HTTPException(404): If the following user is not found.
        :raises HTTPException(409): If they are already following the user.
        :raises HTTPException(400): If the database could not update the list.
        """
        if not await self.user_repo.get_user_by_id(follow_user_id):
            raise HTTPException(status_code=404, detail="User not found!")
        if await self.user_repo.user_is_following_user(user_id, follow_user_id):
            raise HTTPException(status_code=409, detail="Already following that user!")
        result_following, result_followers = await self.user_repo.follow_user_by_id(user_id, follow_user_id)
        if not result_following.raw_result["updatedExisting"] or not result_followers.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update the user followings!")
        return await self.get_user_by_id(user_id)

    async def unfollow_user_by_id(self, user_id: str, unfollow_user_id: str) -> UserOut:
        """
        Allows one user to stop following another by updating their following list.

        :param user_id: The ID of the user who wants to unfollow another user.
        :param unfollow_user_id: The ID of the user to be unfollowed.
        :return: A UserOut object showing the updated details of the user.
        :raises HTTPException(404): If the following user is not found.
        :raises HTTPException(409): If they are not following the user.
        :raises HTTPException(400): If the database could not update the list.
        """
        if not await self.user_repo.get_user_by_id(unfollow_user_id):
            raise HTTPException(status_code=404, detail="User not found!")
        if not await self.user_repo.user_is_following_user(user_id, unfollow_user_id):
            raise HTTPException(status_code=409, detail="Not following that user already!")
        result_following, result_followers = await self.user_repo.unfollow_user_by_id(user_id, unfollow_user_id)
        if not result_following.raw_result["updatedExisting"] or not result_followers.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update the user followings!")
        return await self.get_user_by_id(user_id)

    async def get_following_users_by_id(self, user_id: str) -> UserListOut:
        """
        Retrieves a list of users that the specified user is currently following.

        :param user_id: The ID of the user whose following list is being requested.
        :return: A UserListOut object containing the list of users being followed.
        """
        following_users = []
        user = await self.get_user_by_id(user_id)
        for following_user_id in user.following:
            result = await self.get_user_by_id(following_user_id)
            following_users.append(UserOut(**result.dict()))
        return UserListOut(users=following_users)

    async def get_user_followers_by_id(self, user_id: str) -> UserListOut:
        """
        Retrieves a list of users who are followers of the specified user.

        :param user_id: The ID of the user whose followers are being requested.
        :return: A UserListOut object containing the list of followers.
        """
        user_followers = []
        user = await self.get_user_by_id(user_id)
        for user_follower_id in user.followers:
            result = await self.get_user_by_id(user_follower_id)
            user_followers.append(UserOut(**result.dict()))
        return UserListOut(users=user_followers)

    @staticmethod
    def extract_user_id_from_token(request: Request) -> str:
        """
        Extracts the user ID from the authorization token provided in the request headers.

        :param request: The request object that includes the Authorization header (provided by FastAPI).
        :return: The user ID from the decoded JWT token.
        """
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["sub"]
        return user_id

    @staticmethod
    def get_dietary_criteria() -> DietaryCriteria:
        """
        Retrieves the dietary criteria which include both preferences and restrictions.

        :return: A DietaryCriteria object containing lists of preferences and restrictions.
        """
        return DietaryCriteria(
            preferences=[preference.value for preference in Preferences],
            restrictions=[restriction.value for restriction in Restrictions]
        )

    @staticmethod
    def validate_object_id(object_id: str):
        """
        Validates the objectId.

        :param object_id: The objectId to test.
        :raises HTTPException(422): If the objectId is invalid.
        """
        try:
            ObjectId(object_id)
        except Exception as e:
            logger.error(f"An invalid objectId has been provided: {object_id}")
            raise HTTPException(status_code=422, detail=f"{e}")
