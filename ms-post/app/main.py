# main.py
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List
import os
import jwt

from app.models.Post import Post
from app.models.Comment import Comment
from fastapi import Request

app = FastAPI()

# Initialize MongoDB connection
client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client.your_database_name  # Replace with your actual database name
collection = db.posts

# Helper function to parse MongoDB ObjectId to str and vice versa
def str_to_objectid(item_id: str):
    return ObjectId(item_id)

def post_to_model(post):
    return Post(**post, id=str(post["_id"]))

# CRUD operations for Post

# TODO nowhere is a verification that the user actually exists??
# Just for testing currently
@app.get("/asd")
async def read_root(request: Request):
    # print the whole request
    # print header of request
    # decode bearer token and display payload
    bearer = request.headers.get("Authorization")
    token = bearer.split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    print(payload)
        # decode token
        # print payload
    # decode bearer 
        
    headers = {k: v for k, v in request.headers.items()}
    request_dict = {k: v for k, v in request.query_params.items()}
    return {"Hello": "World1", "request": headers}



@app.post("/", response_model=Post)
async def create_post(post: Post):

    post_dict = post.model_dump(exclude_unset=True)
    post_dict["comments"] = []  # Ensure comments are initialized as an empty list
    result = await collection.insert_one(post_dict)
    post.id = str(result.inserted_id)
    return post

@app.get("/{post_id}", response_model=Post)
async def read_post(post_id: str):
    post = await collection.find_one({"_id": str_to_objectid(post_id)})
    if post:
        return post_to_model(post)
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/{post_id}", response_model=Post)
async def update_post(post_id: str, post: Post):
    updated_post = await collection.find_one_and_update(
        {"_id": str_to_objectid(post_id)}, {"$set": post.dict(exclude_unset=True)}
    )
    if updated_post:
        return await read_post(post_id)
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/{post_id}")
async def delete_post(post_id: str):
    deleted_post = await collection.find_one_and_delete({"_id": str_to_objectid(post_id)})
    if deleted_post:
        return {"status": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")


@app.put("/{post_id}/comment", response_model=Post)
async def add_comment_to_post(post_id: str, comment: Comment):
    await collection.update_one(
        {"_id": str_to_objectid(post_id)},
        {"$push": {"comments": comment.dict()}}
    )
    return await read_post(post_id)

@app.put("/{post_id}/like", response_model=Post)
async def add_like_to_post(post_id: str):
    await collection.update_one(
        {"_id": str_to_objectid(post_id)},
        {"$inc": {"likes": 1}}
    )
    return await read_post(post_id)