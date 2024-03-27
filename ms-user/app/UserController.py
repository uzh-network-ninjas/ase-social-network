from app.models.User import UserOut, UserUpdate
from app.UserService import UserService
from fastapi import FastAPI, Request, UploadFile

app = FastAPI()
us = UserService()

@app.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str) -> UserOut:
    return await us.get_user_by_id(user_id)

@app.get("/", response_model=UserOut)
async def search_user(username: str) -> UserOut:
    return await us.get_user_by_username(username)

@app.patch("/", response_model=UserOut)
async def update_user(request: Request, updated_user: UserUpdate) -> UserOut:
    user_id = us.extract_user_id_from_token(request)
    return await us.update_user_by_id(user_id, updated_user)

@app.patch("/image", response_model=UserOut)
async def update_user_image(request: Request, image: UploadFile) -> UserOut:
    user_id = us.extract_user_id_from_token(request)
    return await us.update_user_image_by_id(user_id, image)

@app.delete("/")
async def delete_user(request: Request) -> dict[str, str]:
    user_id = us.extract_user_id_from_token(request)
    return await us.delete_user_by_id(user_id)

@app.get("/users/{user_id}/following", response_model=None)
async def get_following_users() -> NotImplementedError:
    raise NotImplementedError