from typing import List, Annotated

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewOut import ReviewOut
from app.ReviewService import ReviewService
from fastapi import FastAPI, Request, UploadFile, Form
import requests

app = FastAPI()
rs = ReviewService()


@app.post("/", response_model=ReviewOut)
async def create_review(request: Request, review: ReviewCreate) -> ReviewOut:
    user_id = rs.extract_user_id_from_token(request)
    return await rs.create_review(user_id, review)


@app.patch("/image", response_model=ReviewOut)
async def append_review_image(review_id: Annotated[str, Form()], image: UploadFile) -> ReviewOut:
    return await rs.append_review_image_by_id(review_id, image)


@app.get("/{review_id}", response_model=ReviewOut)
async def get_review(review_id: str) -> ReviewOut:
    return await rs.get_review_by_id(review_id)


@app.get("/")
async def get_feed(request: Request):
    user_id = rs.extract_user_id_from_token(request)
    response = requests.get(f'http://kong:8000/users/{user_id}/following', headers=request.headers)
    # return await rs.get_feed_by_user_id(user_id, response.json())
    return response.json()  # TODO: only returns list of following -> use this to filter reviews by user_ids


@app.get("/")
async def get_reviews_of_places(place_ids: List[str]):
    raise NotImplementedError
