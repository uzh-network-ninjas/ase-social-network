import requests
import os

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewListFilteredOut import ReviewListFilteredOut
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewOut import ReviewOut
from app.models.ReviewUpdate import ReviewUpdate
from app.ReviewService import ReviewService
from app.ReviewRepository import ReviewRepository
from datetime import datetime
from fastapi import FastAPI, Form, Request, UploadFile, status, Query
from typing import Annotated

app = FastAPI()
review_service = ReviewService(ReviewRepository())


@app.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewOut)
async def create_review(request: Request, review: ReviewCreate) -> ReviewOut:
    """Creates a new review.

    :param request: The request object (provided by FastAPI).
    :param review: The review data (ReviewCreate model).
    :return: The created review.

    .. note::
        Pydantic automatically validates the provided data against the model's schema upon instantiation,
        raising a `ValidationError` if the data does not conform to the specified structure and constraints.
    """
    user_id = review_service.extract_user_id_from_token(request)
    username = review_service.extract_username_from_token(request)
    return await review_service.create_review(review, user_id, username)


@app.patch("/image", status_code=status.HTTP_200_OK, response_model=ReviewOut)
async def append_review_image(request: Request, review_id: Annotated[str, Form()], image: UploadFile) -> ReviewOut:
    """Appends an image to an existing review.

    :param request: The request object (provided by FastAPI).
    :param review_id: The ID of the review to which the image will be appended.
    :param image: The image that will be appended.
    :return: The updated review with the appended image.
    """
    review_service.validate_object_id(review_id)
    user_id = review_service.extract_user_id_from_token(request)
    return await review_service.append_review_image_by_id(review_id, image, user_id)


@app.patch("/", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
async def update_review(request: Request, updated_review: ReviewUpdate):
    """
    Updates all reviews written by the user with the newly chosen username

    :param request: The request object (provided by FastAPI)
    :param updated_review: The updated review data (new username).
    """
    user_id = review_service.extract_user_id_from_token(request)
    await review_service.update_review(user_id, updated_review)


@app.get("/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewOut)
async def get_review(request: Request, review_id: str) -> ReviewOut:
    """Get a review by its ID.

    :param request: The request object (provided by FastAPI).
    :param review_id: The ID of the review to retrieve.
    :return: The retrieved review.
    """
    review_service.validate_object_id(review_id)
    user_id = review_service.extract_user_id_from_token(request)
    return await review_service.get_review_by_id(review_id, user_id)


@app.get("/", status_code=status.HTTP_200_OK, response_model=ReviewListOut)
async def get_feed(request: Request, timestamp_cursor: datetime = None) -> ReviewListOut:
    """Get a feed of reviews from the followed users.

    :param request: The request object (provided by FastAPI).
    :param timestamp_cursor: (optional) The cursor for pagination based on timestamps. Defaults to None.
    :return: A list of reviews in the feed.
    """
    user_id = review_service.extract_user_id_from_token(request)
    response = requests.get(f'{os.getenv("GATEWAY_IP", "http://kong:8000")}/users/{user_id}', headers=request.headers)
    return await review_service.get_feed_by_cursor(timestamp_cursor, response.json()["following"], user_id)


@app.get("/users/", status_code=status.HTTP_200_OK, response_model=ReviewListOut)
async def get_reviews_from_user(request: Request, user_id: str) -> ReviewListOut:
    """Get reviews created by a specific user.

    :param request: The request object (provided by FastAPI).
    :param user_id: The ID of the user for the requested reviews.
    :return: A list of reviews created by the user.
    """
    review_service.validate_object_id(user_id)
    extracted_user_id = review_service.extract_user_id_from_token(request)
    return await review_service.get_reviews_by_user_id(user_id, extracted_user_id)


@app.get("/locations/", status_code=status.HTTP_200_OK, response_model=ReviewListFilteredOut)
async def get_filtered_reviews(request: Request, location_id: Annotated[list[str] | None, Query()] = None) -> ReviewListFilteredOut:
    """Get filtered reviews based on location and followed users.

    :param request: The request object (provided by FastAPI).
    :param location_id: (optional) The IDs of the locations to filter by. Defaults to None.
    :return: A list of filtered reviews. If no location_id are provided, all reviews from followed users are returned.

    .. note::
        Pydantic automatically validates the provided data against the model's schema upon instantiation,
        raising a `ValidationError` if the data does not conform to the specified structure and constraints.
    """
    user_id = review_service.extract_user_id_from_token(request)
    response = requests.get(f'{os.getenv("GATEWAY_IP", "http://kong:8000")}/users/{user_id}', headers=request.headers)
    return await review_service.get_reviews_by_locations(location_id, response.json()["following"], user_id)


@app.patch("/{review_id}/likes", status_code=status.HTTP_200_OK, response_model=ReviewOut)
async def like_review(request: Request, review_id: str) -> ReviewOut:
    """Like a review.

    :param request: The request object (provided by FastAPI).
    :param review_id: The ID of the review to like.
    :return: The updated review with the added like.
    """
    review_service.validate_object_id(review_id)
    user_id = review_service.extract_user_id_from_token(request)
    return await review_service.like_review_by_id(review_id, user_id)


@app.delete("/{review_id}/likes", status_code=status.HTTP_200_OK, response_model=ReviewOut)
async def unlike_review(request: Request, review_id: str) -> ReviewOut:
    """Unlike a review.

    :param request: The request object (provided by FastAPI).
    :param review_id: ID of the review to unlike.
    :return: The updated review without the like.
    """
    review_service.validate_object_id(review_id)
    user_id = review_service.extract_user_id_from_token(request)
    return await review_service.unlike_review_by_id(review_id, user_id)
