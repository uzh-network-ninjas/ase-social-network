import boto3
import jwt
import os

from app.logging_config import logger
from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewListFilteredOut import ReviewListFilteredOut, LocationReviews
from app.models.ReviewOut import ReviewOut
from app.models.ReviewUpdate import ReviewUpdate
from app.ReviewRepository import ReviewRepository
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException, Request, UploadFile
from typing import List


class ReviewService:
    def __init__(self, review_repository: ReviewRepository):
        """Initializes the ReviewService with a ReviewRepository instance.

        :param review_repository: An instance of ReviewRepository.
        """
        self.review_repo = review_repository

    async def create_review(self, review: ReviewCreate, user_id: str, username: str) -> ReviewOut:
        """Creates a new review.

        :param review: The review data (ReviewCreate model).
        :param user_id: The ID of the user creating the review.
        :param username: The username of the user creating the review.
        :return: The created review.
        """
        result = await self.review_repo.add_review(review, user_id, username)
        return await self.get_review_by_id(result.inserted_id, user_id)

    async def append_review_image_by_id(self, review_id: str, image: UploadFile, user_id: str) -> ReviewOut:
        """Appends an image to an existing review.

        :param review_id: The ID of the review to which the image will be appended.
        :param image: The image that will be appended.
        :param user_id: The ID of the user appending the image.
        :return: The updated review with the appended image.
        :raises HTTPException(400): If the image could not be uploaded to s3.
        :raises HTTPException(400): If the database could not update the image reference.
        """
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
            logger.error(f"Could not upload an image to s3: {e}")
            raise HTTPException(status_code=400, detail="Could not append review image!")

        updated_review = ReviewUpdate(image=f"{os.getenv("S3_DEFAULT_INSTANCE", "http://localhost:4566")}/{bucket_name}/{object_key}")
        result = await self.review_repo.update_review_by_id(review_id, updated_review)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update review image reference!")
        return await self.get_review_by_id(review_id, user_id)

    async def update_review(self, user_id: str, updated_review: ReviewUpdate):
        """
        Gets all reviews written by the user and updates each with the new username

        :param user_id: The ID of the user.
        :param updated_review: The updated review data (new username).
        """
        reviews_to_update = await self.get_reviews_by_user_id(user_id, "")
        for review in reviews_to_update.reviews:
            result = await self.review_repo.update_review_by_id(review.id, updated_review)
            if not result.raw_result["updatedExisting"]:
                raise HTTPException(status_code=400, detail="Could not update review!")

    async def get_review_by_id(self, review_id: str, user_id: str) -> ReviewOut:
        """Get a review by its ID.

        :param review_id: The ID of the review to retrieve.
        :param user_id: The ID of the user retrieving the review.
        :return: The retrieved review.
        :raises HTTPException(404): If the review could not be found.
        """
        result = await self.review_repo.get_review_by_id(review_id)
        if not result:
            raise HTTPException(status_code=404, detail="Review not found!")
        result["id"] = str(result["_id"])
        result["liked_by_current_user"] = user_id in result["liked_by"]
        return ReviewOut(**result)

    async def get_feed_by_cursor(self, timestamp_cursor: datetime, user_ids: List[str], user_id: str) -> ReviewListOut:
        """Get a feed of reviews from the followed users.

        :param timestamp_cursor: The cursor for pagination based on timestamps. Can be None to use the current timestamp.
        :param user_ids: The list of user IDs of followed users.
        :param user_id: The ID of the user retrieving the feed.
        :return: A list of reviews in the feed.
        :raises HTTPException(404): If the user is not following other users.
        :raises HTTPException(404): If the followed users have not created reviews.
        """
        if len(user_ids) == 0:
            raise HTTPException(status_code=404, detail="No followed users!")
        timestamp_cursor = timestamp_cursor if timestamp_cursor else datetime.now()
        result = await self.review_repo.get_feed_by_cursor_and_user_ids(timestamp_cursor, user_ids, 25)
        if not result:
            raise HTTPException(status_code=404, detail="No reviews from followed users (with that timestamp)!")
        for review in result:
            review["id"] = str(review["_id"])
            review["liked_by_current_user"] = user_id in review["liked_by"]
        return ReviewListOut(reviews=result)

    async def get_reviews_by_user_id(self, user_id: str, current_user_id: str) -> ReviewListOut:
        """Get reviews created by a specific user.

        :param user_id: The ID of the user for the requested reviews.
        :param current_user_id: The ID of the user retrieving the reviews.
        :return: A list of reviews created by the user.
        :raises HTTPException(404): If the user has not created any reviews.
        """
        result = await self.review_repo.get_reviews_by_user_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User has not created any reviews yet!")
        for review in result:
            review["id"] = str(review["_id"])
            review["liked_by_current_user"] = current_user_id in review["liked_by"]
        return ReviewListOut(reviews=result)

    async def get_reviews_by_locations(self, location_ids: List[str], user_ids: List[str],
                                       user_id: str) -> ReviewListFilteredOut:
        """Get filtered reviews based on location and followed users.

        :param location_ids: (optional) The IDs of the locations to filter by. Defaults to None.
        :param user_ids: The list of user IDs of followed users.
        :param user_id: The ID of the user retrieving the filtered reviews.
        :return: A list of filtered reviews. If location_ids is not provided, all reviews from followed users are returned.
        :raises HTTPException(404): If the user is not following other users.
        :raises HTTPException(404): If the followed users have not created reviews.
        :raises HTTPException(404): If no reviews exist for the location and user combination.
        """
        if len(user_ids) == 0:
            raise HTTPException(status_code=404, detail="No followed users!")
        if location_ids is None:
            location_ids = await self.review_repo.get_location_ids_by_user_ids(user_ids)
            if len(location_ids) == 0:
                raise HTTPException(status_code=404, detail="No reviews from the followed users!")
        location_reviews = []
        for location_id in location_ids:
            result = await self.review_repo.get_reviews_by_location_and_user_ids(location_id, user_ids)
            if not result:
                continue
            rating_avg = 0
            for review in result:
                review["id"] = str(review["_id"])
                review["liked_by_current_user"] = user_id in review["liked_by"]
                rating_avg += review["rating"]
            rating_avg /= len(result)
            location_reviews.append(LocationReviews(location_id=location_id, average_rating=rating_avg, reviews=result))
        if len(location_reviews) == 0:
            raise HTTPException(status_code=404, detail="No reviews for this location and user combination!")
        return ReviewListFilteredOut(location_reviews=location_reviews)

    async def like_review_by_id(self, review_id: str, user_id: str) -> ReviewOut:
        """Like a review.

        :param review_id: The ID of the review to like.
        :param user_id: The ID of the user liking a review.
        :return: The updated review with the added like.
        :raises HTTPException(404): If the review does not exist.
        :raises HTTPException(400): If the user has already liked the review.
        :raises HTTPException(400): If the database could not update the like count.
        """
        if not await self.review_repo.get_review_by_id(review_id):
            raise HTTPException(status_code=404, detail="Review not found!")
        if await self.review_repo.user_has_liked_review(review_id, user_id):
            raise HTTPException(status_code=400, detail="User has already liked the review!")
        result = await self.review_repo.like_review_by_id(review_id, user_id)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update the like count!")
        return await self.get_review_by_id(review_id, user_id)

    async def unlike_review_by_id(self, review_id: str, user_id: str) -> ReviewOut:
        """Unlike a review.

        :param review_id: The ID of the review to unlike.
        :param user_id: The ID of the user unliking a review.
        :return: The updated review with the removed like.
        :raises ReviewNotFoundException: If the review does not exist.
        :raises HTTPException(400): If the user has already unliked the review.
        :raises HTTPException(400): If the database could not update the like count.
        """
        if not await self.review_repo.get_review_by_id(review_id):
            raise HTTPException(status_code=404, detail="Review not found!")
        if not await self.review_repo.user_has_liked_review(review_id, user_id):
            raise HTTPException(status_code=400, detail="User has not liked the review already!")
        result = await self.review_repo.unlike_review_by_id(review_id, user_id)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update the like count!")
        return await self.get_review_by_id(review_id, user_id)

    def extract_user_id_from_token(self, request: Request) -> str:
        """Extracts the user ID from the request.

        :param request: The request object.
        :return: The user ID.
        """
        payload = self.extract_payload_from_token(request)
        return payload["sub"]

    def extract_username_from_token(self, request: Request) -> str:
        """Extracts the username from the request.

        :param request: The request object.
        :return: The username.
        """
        payload = self.extract_payload_from_token(request)
        return payload["username"]

    @staticmethod
    def extract_payload_from_token(request: Request) -> dict:
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        return jwt.decode(token, options={"verify_signature": False})

    @staticmethod
    def validate_object_id(object_id: str) -> None:
        """Validates the objectId.

        :param object_id: The objectId to test.
        :raises HTTPException(422): If the objectId is invalid.
        """
        try:
            ObjectId(object_id)
        except Exception as e:
            logger.error(f"An invalid objectId has been provided: {object_id}")
            raise HTTPException(status_code=422, detail=f"{e}")
