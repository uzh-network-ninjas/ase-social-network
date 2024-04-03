import requests

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewOut import ReviewOut
from app.ReviewService import ReviewService
from datetime import datetime
from fastapi import FastAPI, Request, UploadFile, Form
from typing import List, Annotated

app = FastAPI()
rs = ReviewService()


@app.post("/", response_model=ReviewOut)
async def create_review(request: Request, review: ReviewCreate) -> ReviewOut:
    user_id = rs.extract_user_id_from_token(request)
    username = rs.extract_username_from_token(request)
    return await rs.create_review(review, user_id, username)


@app.patch("/image", response_model=ReviewOut)
async def append_review_image(review_id: Annotated[str, Form()], image: UploadFile) -> ReviewOut:
    return await rs.append_review_image_by_id(review_id, image)


@app.get("/{review_id}", response_model=ReviewOut)
async def get_review(review_id: str) -> ReviewOut:
    return await rs.get_review_by_id(review_id)


@app.get("/", response_model=ReviewListOut)
async def get_feed(request: Request, timestamp_cursor: datetime = datetime.now()) -> ReviewListOut:
    user_id = rs.extract_user_id_from_token(request)
    response = requests.get(f'http://kong:8000/users/{user_id}', headers=request.headers)
    return await rs.get_feed_by_cursor_and_followed_users(timestamp_cursor, response.json()["following"])


@app.get("/users/", response_model=ReviewListOut)
async def get_reviews_by_username(username: str) -> ReviewListOut:
    return await rs.get_reviews_by_username(username)


@app.get("/locations/", response_model=ReviewListOut)
async def get_filtered_reviews(location_ids: List[str] = None, usernames: List[str] = None) -> ReviewListOut:
    return await rs.get_reviews_by_locations_and_usernames(location_ids, usernames)