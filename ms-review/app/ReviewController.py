from typing import List, Annotated

from app.models.Review import ReviewCreate, ReviewOut
from ReviewService import ReviewService
from fastapi import FastAPI, Request, UploadFile, Form

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
async def get_feed(request: Request, token: str):
    user_id = rs.extract_user_id_from_token(request)
    raise NotImplementedError

@app.get("/")
async def get_reviews(review_ids: List[str]):
    raise NotImplementedError