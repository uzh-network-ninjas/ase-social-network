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
        self.ur = UserRepository()

    async def get_user_by_id(self, user_id: str) -> UserOut:
        result = await self.ur.get_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    async def get_user_by_username(self, username: str) -> UserOut:
        result = await self.ur.get_user_by_username(username)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    async def update_user_by_id(self, user_id: str, updated_user: UserUpdate) -> UserOut:
        if not await self.ur.get_user_by_id(user_id):
            raise HTTPException(status_code=404, detail="User not found!")
        username = await self.ur.get_user_by_username(updated_user.username)
        email = await self.ur.get_user_by_email(updated_user.email)
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
        result = await self.ur.update_user_by_id(user_id, updated_user)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update user details!")
        return await self.get_user_by_id(user_id)

    async def update_user_image_by_id(self, user_id: str, image: UploadFile) -> UserOut:
        if not await self.ur.get_user_by_id(user_id):
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
        except Exception:
            raise HTTPException(status_code=400, detail="Could not update user profile picture!")

        updated_user = UserUpdate(image=object_key)
        return await self.update_user_by_id(user_id, updated_user)

    async def delete_user_by_id(self, user_id: str):
        result = await self.ur.delete_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")

    async def follow_user_by_id(self, user_id: str, follow_user_id: str) -> UserOut:
        if not await self.ur.get_user_by_id(follow_user_id):
            raise HTTPException(status_code=404, detail="User not found!")
        if await self.ur.user_is_following_user(user_id, follow_user_id):
            raise HTTPException(status_code=409, detail="Already following that user!")
        result_following, result_followers = await self.ur.follow_user_by_id(user_id, follow_user_id)
        if not result_following.raw_result["updatedExisting"] or not result_followers.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update the user followings!")
        return await self.get_user_by_id(user_id)

    async def unfollow_user_by_id(self, user_id: str, unfollow_user_id: str):
        if not await self.ur.get_user_by_id(unfollow_user_id):
            raise HTTPException(status_code=404, detail="User not found!")
        if not await self.ur.user_is_following_user(user_id, unfollow_user_id):
            raise HTTPException(status_code=409, detail="Not following that user already!")
        result_following, result_followers = await self.ur.unfollow_user_by_id(user_id, unfollow_user_id)
        if not result_following.raw_result["updatedExisting"] or not result_followers.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update the user followings!")
        return await self.get_user_by_id(user_id)

    async def get_following_users_by_id(self, user_id: str) -> UserListOut:
        following_users = []
        user = await self.get_user_by_id(user_id)
        for following_user_id in user.following:
            result = await self.get_user_by_id(following_user_id)
            following_users.append(UserOut(**result.dict()))
        return UserListOut(**{"users": following_users})

    async def get_user_followers_by_id(self, user_id: str) -> UserListOut:
        user_followers = []
        user = await self.get_user_by_id(user_id)
        for user_follower_id in user.followers:
            result = await self.get_user_by_id(user_follower_id)
            user_followers.append(UserOut(**result.dict()))
        return UserListOut(**{"users": user_followers})

    @staticmethod
    def extract_user_id_from_token(request: Request) -> str:
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["sub"]
        return user_id

    @staticmethod
    def get_dietary_criteria() -> DietaryCriteria:
        return DietaryCriteria(
            preferences=[preference.value for preference in Preferences],
            restrictions=[restriction.value for restriction in Restrictions]
        )

    @staticmethod
    def validate_object_id(object_id: str):
        """
        Validates the objectId.

        :param object_id: The objectId to test.
        :raise HTTPException(422): If the objectId is invalid.
        """
        try:
            ObjectId(object_id)
        except Exception as e:
            logger.error(f"An invalid objectId has been provided: {object_id}")
            raise HTTPException(status_code=422, detail=f"{e}")
