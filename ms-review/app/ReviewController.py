import requests

from app.models.LocationIDs import LocationIDs
from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewListFilteredOut import ReviewListFilteredOut
from app.models.ReviewOut import ReviewOut
from app.ReviewService import ReviewService
from app.ReviewRepository import ReviewRepository
from datetime import datetime
from fastapi import FastAPI, Request, UploadFile, Form
from typing import Annotated
from app.logging_config import logger

app = FastAPI()
rs = ReviewService(ReviewRepository())


@app.post("/", response_model=ReviewOut)
async def create_review(request: Request, review: ReviewCreate) -> ReviewOut:
    user_id = rs.extract_user_id_from_token(request)
    username = rs.extract_username_from_token(request)
    return await rs.create_review(review, user_id, username)


@app.patch("/image", response_model=ReviewOut)
async def append_review_image(request: Request, review_id: Annotated[str, Form()], image: UploadFile) -> ReviewOut:
    user_id = rs.extract_user_id_from_token(request)
    return await rs.append_review_image_by_id(review_id, image, user_id)


@app.get("/{review_id}", response_model=ReviewOut)
async def get_review(request: Request, review_id: str) -> ReviewOut:
    user_id = rs.extract_user_id_from_token(request)
    return await rs.get_review_by_id(review_id, user_id)


@app.get("/", response_model=ReviewListOut)
async def get_feed(request: Request, timestamp_cursor: datetime = None) -> ReviewListOut:
    user_id = rs.extract_user_id_from_token(request)
    response = requests.get(f'http://kong:8000/users/{user_id}', headers=request.headers)
    return await rs.get_feed_by_cursor(timestamp_cursor, response.json()["following"], user_id)


@app.get("/users/", response_model=ReviewListOut)
async def get_reviews_from_user(request: Request, user_id: str) -> ReviewListOut:
    extracted_user_id = rs.extract_user_id_from_token(request)
    return await rs.get_reviews_by_user_id(user_id, extracted_user_id)


@app.get("/locations/", response_model=ReviewListFilteredOut)
async def get_filtered_reviews(request: Request, location_ids: LocationIDs = None) -> ReviewListFilteredOut:
    user_id = rs.extract_user_id_from_token(request)
    headers = {k: v for k, v in request.headers.items() if k not in ("content-type", "content-length")}
    response = requests.get(f'http://kong:8000/users/{user_id}', headers=headers)
    return await rs.get_reviews_by_locations(location_ids, response.json()["following"], user_id)


@app.patch("/{review_id}/likes", response_model=ReviewOut)
async def like_review(request: Request, review_id: str) -> ReviewOut:
    user_id = rs.extract_user_id_from_token(request)
    return await rs.like_review_by_id(review_id, user_id)


@app.delete("/{review_id}/likes", response_model=ReviewOut)
async def unlike_review(request: Request, review_id: str) -> ReviewOut:
    user_id = rs.extract_user_id_from_token(request)
    return await rs.unlike_review_by_id(review_id, user_id)