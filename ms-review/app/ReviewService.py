import boto3
import jwt
import os

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewOut import ReviewOut
from app.ReviewRepository import ReviewRepository
from fastapi import HTTPException, Request, UploadFile
from typing import List

class ReviewService:
    def __init__(self):
        self.rr = ReviewRepository()

    async def create_review(self, user_id: str, review: ReviewCreate):
        raise NotImplementedError

    async def append_review_image_by_id(self, review_id: str, image: UploadFile):
        raise NotImplementedError

    async def get_review_by_id(self, review_id: str):
        raise NotImplementedError

    async def get_feed_by_token(self, token):
        raise NotImplementedError

    async def get_reviews_by_ids(self, review_ids: List[str]):
        raise NotImplementedError

    @staticmethod
    def extract_user_id_from_token(request: Request) -> str:
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["sub"]
        return user_id