import boto3
import jwt
import os

from app.models.UserUpdate import UserUpdate
from app.models.UserOut import UserOut
from app.models.UserListOut import UserListOut
from app.UserRepository import UserRepository
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
        result = await self.ur.update_user_by_id(user_id, updated_user)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update user details!")
        return await self.get_user_by_id(user_id)

    async def update_user_image_by_id(self, user_id: str, image: UploadFile) -> UserOut:
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
        except:
            raise HTTPException(status_code=400, detail="Could not update user profile picture!")

        updated_user = UserUpdate(image=object_key)
        return await self.update_user_by_id(user_id, updated_user)

    async def delete_user_by_id(self, user_id: str):
        result = await self.ur.delete_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")

    async def follow_user_by_id(self, user_id: str, follow_user_id: str) -> UserOut:
        user_to_follow = await self.get_user_by_id(follow_user_id)
        curr_user = await self.get_user_by_id(user_id)
        if follow_user_id in curr_user.following:
            raise HTTPException(status_code=409, detail="User already followed")
        user_to_follow.followers.append(user_id)
        _ = await self.update_user_by_id(follow_user_id, UserUpdate(**user_to_follow.dict()))
        curr_user.following.append(follow_user_id)
        return await self.update_user_by_id(user_id, UserUpdate(**curr_user.dict()))

    async def unfollow_user_by_id(self, user_id: str, unfollow_user_id: str):
        user_to_unfollow = await self.get_user_by_id(unfollow_user_id)
        curr_user = await self.get_user_by_id(user_id)
        if unfollow_user_id not in curr_user.following:
            raise HTTPException(status_code=404, detail="User is not followed")
        curr_user.following.remove(unfollow_user_id)
        _ = await self.update_user_by_id(user_id, UserUpdate(**curr_user.dict()))
        user_to_unfollow.followers.remove(user_id)
        _ = await self.update_user_by_id(unfollow_user_id, UserUpdate(**user_to_unfollow.dict()))

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
