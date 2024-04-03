import json

import boto3
import jwt
import os

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewOut import ReviewOut
from app.models.ReviewCreateImage import ReviewCreateImage
from app.ReviewRepository import ReviewRepository
from datetime import datetime
from fastapi import HTTPException, Request, UploadFile
from typing import List


class ReviewService:
    def __init__(self):
        self.rr = ReviewRepository()


    async def create_review(self, review: ReviewCreate, user_id: str, username: str) -> ReviewOut:
        result = await self.rr.add_review(review, user_id, username)
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
        except Exception:
            raise HTTPException(status_code=400, detail="Could not append review image!")

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


    async def get_feed_by_cursor_and_followed_users(self, timestamp_cursor: datetime, user_ids: List[str]) -> ReviewListOut:
        if len(user_ids) == 0:
            raise HTTPException(status_code=404, detail="No users found")
        page_size = 25
        reviews = await self.rr.get_feed_by_cursor_and_user_ids(timestamp_cursor, user_ids, page_size)
        if len(reviews) == 0:
            raise HTTPException(status_code=404, detail="No reviews found")
        for review in reviews:
            review["id"] = str(review["_id"])
        return ReviewListOut(reviews=reviews)


    async def get_reviews_by_username(self, username: str) -> ReviewListOut:
        result = await self.rr.get_reviews_by_username(username)
        if not result:
            raise HTTPException(status_code=404, detail="User has not created any reviews yet!")
        for review in result:
            review["id"] = str(review["_id"])
        return ReviewListOut(reviews=result)


    async def get_reviews_by_locations_and_usernames(self, location_ids: List[str], usernames: List[str]) -> ReviewListOut:
        result = await self.rr.get_reviews_by_locations_and_usernames(location_ids, usernames)
        if not result:
            raise HTTPException(status_code=404, detail="No reviews for this location and user combination!")
        for review in result:
            review["id"] = str(review["_id"])
        return ReviewListOut(reviews=result)


    def extract_user_id_from_token(self, request: Request) -> str:
        payload = self.extract_payload_from_token(request)
        return payload["sub"]


    def extract_username_from_token(self, request: Request) -> str:
        payload = self.extract_payload_from_token(request)
        return payload["username"]


    @staticmethod
    def extract_payload_from_token(request: Request) -> dict:
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        return jwt.decode(token, options={"verify_signature": False})