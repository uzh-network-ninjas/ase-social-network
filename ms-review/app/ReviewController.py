from typing import List, Annotated

from app.models.Review import ReviewCreate, ReviewOut
from app.ReviewService import ReviewService
from fastapi import FastAPI, Request, UploadFile, Form

app = FastAPI()
rs = ReviewService()

@app.post("/")
async def create_review(request: Request):
    user_id = rs.extract_user_id_from_token(request)
    raise NotImplementedError

@app.patch("/image")
async def append_review_image(review_id: Annotated[str, Form()], image: UploadFile):
    raise NotImplementedError

@app.get("/{review_id}")
async def get_review(review_id: str):
    raise NotImplementedError

@app.get("/")
async def get_feed(request: Request, token: str):
    user_id = rs.extract_user_id_from_token(request)
    raise NotImplementedError

@app.get("/")
async def get_reviews(review_ids: List[str]):
    raise NotImplementedError