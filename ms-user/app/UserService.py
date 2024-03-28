import boto3
import jwt
import os

from app.models.User import UserOut, UserUpdate
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
        result = await self.ur.update_user_by_id(user_id, updated_user)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update user profile picture reference!")
        return await self.get_user_by_id(user_id)

    async def delete_user_by_id(self, user_id: str):
        result = await self.ur.delete_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")

    @staticmethod
    def extract_user_id_from_token(request: Request) -> str:
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["sub"]
        return user_id
