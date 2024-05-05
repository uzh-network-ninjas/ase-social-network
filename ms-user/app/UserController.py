import requests
import os

from app.models.DietaryCriteria import DietaryCriteria
from app.models.UserUpdate import UserUpdate
from app.models.UserOut import UserOut
from app.models.UserListOut import UserListOut
from app.UserService import UserService
from fastapi import FastAPI, Request, UploadFile, status

app = FastAPI()
user_service = UserService()


@app.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(user_id: str) -> UserOut:
    """
    Retrieves a user's details by their ID.

    :param user_id: The ID of the user.
    :return: A UserOut object containing the user's detailed information.
    """
    user_service.validate_object_id(user_id)
    return await user_service.get_user_by_id(user_id)


@app.get("/", status_code=status.HTTP_200_OK, response_model=UserOut)
async def search_user(username: str) -> UserOut:
    """
    Searches for and retrieves a user's details by their username.

    :param username: The name of the user to search for.
    :return: A UserOut object containing the user's detailed information.
    """
    return await user_service.get_user_by_username(username)


@app.patch("/", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user(request: Request, updated_user: UserUpdate) -> UserOut:
    """
    Updates a user's profile information.

    :param request: The request used to extract the user's ID from the token.
    :param updated_user: The updated user data.
    :return: A UserOut object showing the updated user details.
    """
    user_id = user_service.extract_user_id_from_token(request)
    user = await user_service.update_user_by_id(user_id, updated_user)
    if updated_user.username:
        requests.patch(f'{os.getenv("GATEWAY_IP", "http://kong:8000")}/reviews/', headers=request.headers, json={"username": user.username})
    return user


@app.patch("/image", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user_image(request: Request, image: UploadFile) -> UserOut:
    """
    Updates a user's profile image.

    :param request: The request used to extract the user's ID from the token.
    :param image: The image file to be uploaded.
    :return: A UserOut object showing the updated user details.
    """
    user_id = user_service.extract_user_id_from_token(request)
    return await user_service.update_user_image_by_id(user_id, image)


@app.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request):
    """
    Deletes a user's account.

    :param request: The request used to extract the user's ID from the token.
    """
    user_id = user_service.extract_user_id_from_token(request)
    await user_service.delete_user_by_id(user_id)


@app.get("/{user_id}/following", status_code=status.HTTP_200_OK, response_model=UserListOut)
async def get_following_users(user_id: str) -> UserListOut:
    """
    Retrieves a list of users that the specified user is following.

    :param user_id: The user's ID.
    :return: A UserListOut object containing a list of followed users.
    """
    user_service.validate_object_id(user_id)
    return await user_service.get_following_users_by_id(user_id)


@app.get("/{user_id}/followers", status_code=status.HTTP_200_OK, response_model=UserListOut)
async def get_user_followers(user_id: str) -> UserListOut:
    """
    Retrieves a list of users following the specified user.

    :param user_id: The user's ID.
    :return: A UserListOut object containing a list of followers.
    """
    user_service.validate_object_id(user_id)
    return await user_service.get_user_followers_by_id(user_id)


@app.patch("/following/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def follow_user(request: Request, user_id: str) -> UserOut:
    """
    Allows the current user to follow another user.

    :param request: The request used to extract the current user's ID from the token.
    :param user_id: The ID of the user to be followed.
    :return: A UserOut object showing the current user's updated details.
    """
    user_service.validate_object_id(user_id)
    curr_user_id = user_service.extract_user_id_from_token(request)
    return await user_service.follow_user_by_id(curr_user_id, user_id)


@app.delete("/following/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def unfollow_user(request: Request, user_id: str) -> UserOut:
    """
    Allows the current user to unfollow another user.

    :param request: The request used to extract the current user's ID from the token.
    :param user_id: The ID of the user to be unfollowed.
    :return: A UserOut object showing the current user's updated details.
    """
    user_service.validate_object_id(user_id)
    curr_user_id = user_service.extract_user_id_from_token(request)
    return await user_service.unfollow_user_by_id(curr_user_id, user_id)


@app.get("/dietary_criteria/", status_code=status.HTTP_200_OK, response_model=DietaryCriteria)
def get_dietary_criteria() -> DietaryCriteria:
    """
    Retrieves dietary criteria information from the system.

    :return: A DietaryCriteria object containing restrictions and preferences.
    """
    return user_service.get_dietary_criteria()
