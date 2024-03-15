import jwt

from fastapi import FastAPI, Request
from app.models.User import UserOut, UserUpdate
from app.UserService import UserService

app = FastAPI()
us = UserService()

@app.patch("/", response_model=UserOut)
async def update_user(request: Request, updated_user: UserUpdate):
    bearer = request.headers.get("Authorization")
    token = bearer.split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    user_id = payload["sub"]
    return await us.update_user_by_id(user_id, updated_user)

@app.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    return await us.get_user_by_id(user_id)

@app.get("/", response_model=UserOut)
async def search_user(username: str):
    return await us.get_user_by_username(username)

@app.delete("/")
async def delete_user(request: Request):
    bearer = request.headers.get("Authorization")
    token = bearer.split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    user_id = payload["sub"]
    return await us.delete_user_by_id(user_id)

@app.get("/users/{user_id}/following", response_model=None)
async def get_following_users():
    raise NotImplementedError