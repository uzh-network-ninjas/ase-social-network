from app.models.DietaryCriteria import DietaryCriteria
from app.models.UserUpdate import UserUpdate
from app.models.UserOut import UserOut
from app.models.UserListOut import UserListOut
from app.UserService import UserService
from fastapi import FastAPI, Request, UploadFile, status
from app.logging_config import logger

app = FastAPI()
us = UserService()


@app.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(user_id: str) -> UserOut:
    return await us.get_user_by_id(user_id)


@app.get("/", status_code=status.HTTP_200_OK, response_model=UserOut)
async def search_user(username: str) -> UserOut:
    return await us.get_user_by_username(username)


@app.patch("/", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user(request: Request, updated_user: UserUpdate) -> UserOut:
    user_id = us.extract_user_id_from_token(request)
    return await us.update_user_by_id(user_id, updated_user)


@app.patch("/image", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user_image(request: Request, image: UploadFile) -> UserOut:
    user_id = us.extract_user_id_from_token(request)
    return await us.update_user_image_by_id(user_id, image)


@app.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request):
    user_id = us.extract_user_id_from_token(request)
    await us.delete_user_by_id(user_id)


@app.get("/{user_id}/following", status_code=status.HTTP_200_OK, response_model=UserListOut)
async def get_following_users(user_id: str) -> UserListOut:
    return await us.get_following_users_by_id(user_id)


@app.get("/{user_id}/followers", status_code=status.HTTP_200_OK, response_model=UserListOut)
async def get_user_followers(user_id: str) -> UserListOut:
    return await us.get_user_followers_by_id(user_id)


@app.patch("/following/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def follow_user(request: Request, user_id: str) -> UserOut:
    curr_user_id = us.extract_user_id_from_token(request)
    return await us.follow_user_by_id(curr_user_id, user_id)


@app.delete("/following/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def unfollow_user(request: Request, user_id: str) -> UserOut:
    curr_user_id = us.extract_user_id_from_token(request)
    return await us.unfollow_user_by_id(curr_user_id, user_id)


@app.get("/dietary_criteria/", response_model=DietaryCriteria)
def get_dietary_criteria() -> DietaryCriteria:
    return us.get_dietary_criteria()
