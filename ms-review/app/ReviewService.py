import boto3
import jwt
import os

from app.models.Review import ReviewCreate, ReviewCreateImage, ReviewOut
from app.ReviewRepository import ReviewRepository
from fastapi import HTTPException, Request, UploadFile
from typing import List

class ReviewService:
    def __init__(self):
        self.rr = ReviewRepository()

    async def create_review(self, user_id: str, review: ReviewCreate) -> ReviewOut:
        result = await self.rr.add_review(user_id, review)
        return await self.get_review_by_id(result.inserted_id)

    async def append_review_image_by_id(self, review_id: str, image: UploadFile) -> ReviewOut:
        bucket_name = "ms-review"
        s3_folder = "review-images"
        s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )

        try:
            file_content = await image.read()
            object_key = f"{s3_folder}/{review_id}/{image.filename}"
            s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Could not append review image!" + str(e))

        updated_review = ReviewCreateImage(image=object_key)
        result = await self.rr.update_review_image(review_id, updated_review)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update review image reference!")
        return await self.get_review_by_id(review_id)

    async def get_review_by_id(self, review_id: str) -> ReviewOut:
        result = await self.rr.get_review_by_id(review_id)
        if not result:
            raise HTTPException(status_code=404, detail="Review not found!")
        result["id"] = str(result["_id"])
        return ReviewOut(**result)

    async def get_feed_by_token(self, token):
        raise NotImplementedError

    async def get_reviews_by_place_ids(self, place_ids: List[str]):
        raise NotImplementedError

    @staticmethod
    def extract_user_id_from_token(request: Request) -> str:
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["sub"]
        return user_id