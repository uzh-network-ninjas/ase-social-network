import requests

from app.models.LocationIDs import LocationIDs
from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewListFilteredOut import ReviewListFilteredOut
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewOut import ReviewOut
from app.ReviewService import ReviewService
from app.ReviewRepository import ReviewRepository
from datetime import datetime
from fastapi import FastAPI, Form, Request, UploadFile
from typing import Annotated

app = FastAPI()
rs = ReviewService(ReviewRepository())


@app.post("/", response_model=ReviewOut)
async def create_review(request: Request, review: ReviewCreate) -> ReviewOut:
    """Creates a new review.

    :param request: The request object (provided by FastAPI).
    :param review: The review data (ReviewCreate model).
    :return: The created review.

    .. note::
        Pydantic automatically validates the provided data against the model's schema upon instantiation,
        raising a `ValidationError` if the data does not conform to the specified structure and constraints.
    """
    user_id = rs.extract_user_id_from_token(request)
    username = rs.extract_username_from_token(request)
    return await rs.create_review(review, user_id, username)


@app.patch("/image", response_model=ReviewOut)
async def append_review_image(request: Request, review_id: Annotated[str, Form()], image: UploadFile) -> ReviewOut:
    """Appends an image to an existing review.

    :param request: The request object (provided by FastAPI).
    :param review_id: The ID of the review to which the image will be appended.
    :param image: The image that will be appended.
    :return: The updated review with the appended image.
    """
    rs.validate_object_id(review_id)
    user_id = rs.extract_user_id_from_token(request)
    return await rs.append_review_image_by_id(review_id, image, user_id)


@app.get("/{review_id}", response_model=ReviewOut)
async def get_review(request: Request, review_id: str) -> ReviewOut:
    """Get a review by its ID.

    :param request: The request object (provided by FastAPI).
    :param review_id: The ID of the review to retrieve.
    :return: The retrieved review.
    """
    rs.validate_object_id(review_id)
    user_id = rs.extract_user_id_from_token(request)
    return await rs.get_review_by_id(review_id, user_id)


@app.get("/", response_model=ReviewListOut)
async def get_feed(request: Request, timestamp_cursor: datetime = None) -> ReviewListOut:
    """Get a feed of reviews from the followed users.

    :param request: The request object (provided by FastAPI).
    :param timestamp_cursor: (optional) The cursor for pagination based on timestamps. Defaults to None.
    :return: A list of reviews in the feed.
    """
    user_id = rs.extract_user_id_from_token(request)
    response = requests.get(f'http://kong:8000/users/{user_id}', headers=request.headers)
    return await rs.get_feed_by_cursor(timestamp_cursor, response.json()["following"], user_id)


@app.get("/users/", response_model=ReviewListOut)
async def get_reviews_from_user(request: Request, user_id: str) -> ReviewListOut:
    """Get reviews created by a specific user.

    :param request: The request object (provided by FastAPI).
    :param user_id: The ID of the user for the requested reviews.
    :return: A list of reviews created by the user.
    """
    rs.validate_object_id(user_id)
    extracted_user_id = rs.extract_user_id_from_token(request)
    return await rs.get_reviews_by_user_id(user_id, extracted_user_id)


@app.get("/locations/", response_model=ReviewListFilteredOut)
async def get_filtered_reviews(request: Request, location_ids: LocationIDs = None) -> ReviewListFilteredOut:
    """Get filtered reviews based on location and followed users.

    :param request: The request object (provided by FastAPI).
    :param location_ids: (optional) The IDs of the locations to filter by. Defaults to None.
    :return: A list of filtered reviews. If location_ids is not provided, all reviews from followed users are returned.

    .. note::
        Pydantic automatically validates the provided data against the model's schema upon instantiation,
        raising a `ValidationError` if the data does not conform to the specified structure and constraints.
    """
    user_id = rs.extract_user_id_from_token(request)
    headers = {k: v for k, v in request.headers.items() if k not in ("content-type", "content-length")}
    response = requests.get(f'http://kong:8000/users/{user_id}', headers=headers)
    return await rs.get_reviews_by_locations(location_ids, response.json()["following"], user_id)


@app.patch("/{review_id}/likes", response_model=ReviewOut)
async def like_review(request: Request, review_id: str) -> ReviewOut:
    """Like a review.

    :param request: The request object (provided by FastAPI).
    :param review_id: The ID of the review to like.
    :return: The updated review with the added like.
    """
    rs.validate_object_id(review_id)
    user_id = rs.extract_user_id_from_token(request)
    return await rs.like_review_by_id(review_id, user_id)


@app.delete("/{review_id}/likes", response_model=ReviewOut)
async def unlike_review(request: Request, review_id: str) -> ReviewOut:
    """Unlike a review.

    :param request: The request object (provided by FastAPI).
    :param review_id: ID of the review to unlike.
    :return: The updated review without the like.
    """
    rs.validate_object_id(review_id)
    user_id = rs.extract_user_id_from_token(request)
    return await rs.unlike_review_by_id(review_id, user_id)
