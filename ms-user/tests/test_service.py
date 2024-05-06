import pytest
from unittest.mock import MagicMock, patch
from app.UserService import UserService
from app.models.UserOut import UserOut
from app.models.UserUpdate import UserUpdate
from app.models.Preferences import Preferences
from app.models.Restrictions import Restrictions
from fastapi import HTTPException, UploadFile, Request
from datetime import datetime
from pymongo.results import UpdateResult

user_service = UserService()
test_user_id = "test_user_id"
test_user_id_second = "test_user_id_second"
test_username = "test_user"
test_username_second = "test_user_second"
test_user = {
    "_id": test_user_id,
    "username": test_username,
    "email": "test@example.com",
    "created_at": datetime.now(),
    "image": None,
    "preferences": [],
    "restrictions": [],
    "following": [],
    "followers": [],
    "updated_at": None
}
test_invalid_user = {
    "_id": test_user_id,
    "username": test_username,
    "email": "test@example.com",
    "created_at": datetime.now(),
    "image": None,
    "preferences": ["Preference 1", "Preference 2"],
    "restrictions": ["Restriction 1", "Restriction 2"],
    "following": [],
    "followers": [],
    "updated_at": None
}
test_user_second = {
    "id": test_user_id_second,
    "username": test_username_second,
    "email": "test_second@example.com",
    "created_at": datetime.now(),
    "image": None,
    "preferences": [],
    "restrictions": [],
    "following": [],
    "followers": [],
    "updated_at": None
}
test_user_update = {
    "id": test_user_id,
    "username": test_username,
    "email": "test@example.com",
    "created_at": datetime.now(),
    "image": f"user-images/{test_user_id}/test_image.jpg",
    "preferences": [],
    "restrictions": [],
    "following": [test_user_id_second],
    "followers": [test_user_id_second],
    "updated_at": datetime.now()
}
dummy_update_result = UpdateResult(
    raw_result={"updatedExisting": True},
    acknowledged=True
)
dummy_no_update_result = UpdateResult(
    raw_result={"updatedExisting": False},
    acknowledged=True
)
test_follow = {
    "users": [UserOut(**test_user_update)]
}
test_dietary = {
    "preferences": ["Fast Food", "Fusion"],
    "restrictions": ["Vegetarian", "Vegan"]
}


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
async def test_service_get_user_by_id_success(mock_get_user_by_id):
    mock_get_user_by_id.return_value = test_user
    fetched_user = await user_service.get_user_by_id(test_user_id)
    assert test_user.get('_id') == fetched_user.id
    assert test_user.get('username') == fetched_user.username
    assert test_user.get('email') == fetched_user.email
    assert test_user.get('created_at') == fetched_user.created_at


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
async def test_service_get_user_by_id_not_found(mock_get_user_by_id):
    mock_get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.get_user_by_id(test_user_id)
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_username')
async def test_service_get_user_by_username_success(mock_get_user_by_username):
    mock_get_user_by_username.return_value = test_user
    fetched_user = await user_service.get_user_by_username(test_user_id)
    assert test_user.get('_id') == fetched_user.id
    assert test_user.get('username') == fetched_user.username
    assert test_user.get('email') == fetched_user.email
    assert test_user.get('created_at') == fetched_user.created_at


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_username')
async def test_service_get_user_by_username_not_found(mock_get_user_by_username):
    mock_get_user_by_username.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.get_user_by_username(test_user_id)
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.get_user_by_username')
@patch('app.UserRepository.UserRepository.get_user_by_email')
@patch('app.UserRepository.UserRepository.update_user_by_id')
@patch('app.UserService.UserService.get_user_by_id')
async def test_service_update_user_by_id_success(
        mock_service_get_user_by_id,
        mock_update_user_by_id,
        mock_get_user_by_email,
        mock_get_user_by_username,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user
    mock_get_user_by_username.return_value = None
    mock_get_user_by_email.return_value = None
    mock_update_user_by_id.return_value = dummy_update_result
    mock_service_get_user_by_id.return_value = UserOut(**test_user_second)
    updated_user = await user_service.update_user_by_id(test_user_id, UserUpdate(**test_user_second))
    assert test_user_second.get('id') == updated_user.id
    assert test_user_second.get('username') == updated_user.username
    assert test_user_second.get('email') == updated_user.email
    assert test_user_second.get('created_at') == updated_user.created_at


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
async def test_service_update_user_by_id_not_found(mock_repo_get_user_by_id):
    mock_repo_get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_by_id(test_user_id, UserUpdate(**test_user_second))
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.get_user_by_username')
@patch('app.UserRepository.UserRepository.get_user_by_email')
async def test_service_update_user_by_id_update_exists(
        mock_get_user_by_email,
        mock_get_user_by_username,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user
    # username already taken
    mock_get_user_by_username.return_value = test_user_second
    mock_get_user_by_email.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_by_id(test_user_id, UserUpdate(**test_user_second))
    assert e.value.status_code == 400
    # user email already taken
    mock_get_user_by_username.return_value = None
    mock_get_user_by_email.return_value = test_user_second
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_by_id(test_user_id, UserUpdate(**test_user_second))
    assert e.value.status_code == 400
    # username and email already taken
    mock_get_user_by_username.return_value = test_user_second
    mock_get_user_by_email.return_value = test_user_second
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_by_id(test_user_id, UserUpdate(**test_user_second))
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.get_user_by_username')
@patch('app.UserRepository.UserRepository.get_user_by_email')
async def test_service_update_user_by_id_invalid_preferences_and_restrictions(
        mock_get_user_by_email,
        mock_get_user_by_username,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user
    mock_get_user_by_username.return_value = None
    mock_get_user_by_email.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_by_id(test_user_id, UserUpdate(**test_invalid_user))
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.get_user_by_username')
@patch('app.UserRepository.UserRepository.get_user_by_email')
@patch('app.UserRepository.UserRepository.update_user_by_id')
@patch('app.UserService.UserService.get_user_by_id')
async def test_service_update_user_by_id_not_updated(
        mock_service_get_user_by_id,
        mock_update_user_by_id,
        mock_get_user_by_email,
        mock_get_user_by_username,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user
    mock_get_user_by_username.return_value = None
    mock_get_user_by_email.return_value = None
    mock_update_user_by_id.return_value = dummy_no_update_result
    mock_service_get_user_by_id.return_value = UserOut(**test_user_second)
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_by_id(test_user_id, UserUpdate(**test_user_second))
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('boto3.client')
@patch('app.UserService.UserService.update_user_by_id')
async def test_service_update_user_image_by_id_success(mock_update_user_by_id, mock_boto3_client, mock_get_user_by_id):
    mock_get_user_by_id.return_value = test_user
    mock_boto3_client.return_value = MagicMock()
    mock_image = MagicMock(spec=UploadFile)
    mock_image.filename = "test_image.jpg"
    mock_image.read.return_value = "mock image"
    mock_update_user_by_id.return_value = UserOut(**test_user_update)
    updated_user = await user_service.update_user_image_by_id(test_user_id, mock_image)
    assert test_user_update.get('image') == updated_user.image


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
async def test_service_update_user_image_by_id_not_found(mock_get_user_by_id):
    mock_get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_image_by_id(test_user_id, MagicMock(spec=UploadFile))
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch("app.logging_config.logger.error", return_value=None)
@patch('boto3.client')
async def test_service_update_user_image_by_id_faulty_boto(mock_boto3_client, mock_logger_error, mock_get_user_by_id):
    mock_get_user_by_id.return_value = test_user
    mock_boto3_client.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_image_by_id(test_user_id, MagicMock(spec=UploadFile))
    mock_logger_error.assert_called_once()
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch("app.logging_config.logger.error", return_value=None)
@patch('boto3.client')
async def test_service_update_user_image_by_id_corrupt_image(mock_boto3_client, mock_logger_error, mock_get_user_by_id):
    mock_get_user_by_id.return_value = test_user
    mock_boto3_client.return_value = MagicMock()
    mock_image = MagicMock(spec=UploadFile)
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_image_by_id(test_user_id, mock_image)
    mock_logger_error.assert_called_once()
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.delete_user_by_id')
async def test_service_delete_user_by_id_success(mock_delete_user_by_id):
    mock_delete_user_by_id.return_value = test_user
    await user_service.delete_user_by_id(test_user_id)
    mock_delete_user_by_id.assert_called_once()


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.delete_user_by_id')
async def test_service_delete_user_by_id_not_found(mock_delete_user_by_id):
    mock_delete_user_by_id.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.delete_user_by_id(test_user_id)
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.user_is_following_user')
@patch('app.UserRepository.UserRepository.follow_user_by_id')
@patch('app.UserService.UserService.get_user_by_id')
async def test_service_follow_user_by_id_success(
        mock_service_get_user_by_id,
        mock_follow_user_by_id,
        mock_user_is_following_user,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user_second
    mock_user_is_following_user.return_value = False
    mock_follow_user_by_id.return_value = (dummy_update_result, dummy_update_result)
    mock_service_get_user_by_id.return_value = UserOut(**test_user_update)
    fetched_user = await user_service.follow_user_by_id(test_user_id, test_user_id_second)
    assert test_user_update.get('following') == fetched_user.following


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
async def test_service_follow_user_by_id_not_found(
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.follow_user_by_id(test_user_id, test_user_id_second)
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.user_is_following_user')
async def test_service_follow_user_by_id_already_following(
        mock_user_is_following_user,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user_second
    mock_user_is_following_user.return_value = True
    with pytest.raises(HTTPException) as e:
        await user_service.follow_user_by_id(test_user_id, test_user_id_second)
    assert e.value.status_code == 409


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.user_is_following_user')
@patch('app.UserRepository.UserRepository.follow_user_by_id')
async def test_service_follow_user_by_id_not_updated(
        mock_follow_user_by_id,
        mock_user_is_following_user,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user_second
    mock_user_is_following_user.return_value = False
    mock_follow_user_by_id.return_value = (dummy_update_result, dummy_no_update_result)
    with pytest.raises(HTTPException) as e:
        await user_service.follow_user_by_id(test_user_id, test_user_id_second)
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.user_is_following_user')
@patch('app.UserRepository.UserRepository.unfollow_user_by_id')
@patch('app.UserService.UserService.get_user_by_id')
async def test_service_unfollow_user_by_id_success(
        mock_service_get_user_by_id,
        mock_unfollow_user_by_id,
        mock_user_is_following_user,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user_second
    mock_user_is_following_user.return_value = True
    mock_unfollow_user_by_id.return_value = (dummy_update_result, dummy_update_result)
    mock_service_get_user_by_id.return_value = UserOut(**test_user)
    fetched_user = await user_service.unfollow_user_by_id(test_user_id, test_user_id_second)
    assert test_user.get('following') == fetched_user.following


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
async def test_service_unfollow_user_by_id_not_found(
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as e:
        await user_service.unfollow_user_by_id(test_user_id, test_user_id_second)
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.user_is_following_user')
async def test_service_unfollow_user_by_id_not_following(
        mock_user_is_following_user,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user_second
    mock_user_is_following_user.return_value = False
    with pytest.raises(HTTPException) as e:
        await user_service.unfollow_user_by_id(test_user_id, test_user_id_second)
    assert e.value.status_code == 409


@pytest.mark.asyncio
@patch('app.UserRepository.UserRepository.get_user_by_id')
@patch('app.UserRepository.UserRepository.user_is_following_user')
@patch('app.UserRepository.UserRepository.unfollow_user_by_id')
async def test_service_unfollow_user_by_id_not_updated(
        mock_unfollow_user_by_id,
        mock_user_is_following_user,
        mock_repo_get_user_by_id
):
    mock_repo_get_user_by_id.return_value = test_user_second
    mock_user_is_following_user.return_value = True
    mock_unfollow_user_by_id.return_value = (dummy_update_result, dummy_no_update_result)
    with pytest.raises(HTTPException) as e:
        await user_service.unfollow_user_by_id(test_user_id, test_user_id_second)
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_id')
async def test_service_get_following_users_by_id_success(mock_get_user_by_id):
    mock_get_user_by_id.return_value = UserOut(**test_user_update)
    fetched_users = await user_service.get_following_users_by_id(test_user_id)
    assert test_follow.get('users') == fetched_users.users


@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_id')
async def test_service_get_user_followers_by_id_success(mock_get_user_by_id):
    mock_get_user_by_id.return_value = UserOut(**test_user_update)
    fetched_users = await user_service.get_user_followers_by_id(test_user_id)
    assert test_follow.get('users') == fetched_users.users


@patch("jwt.decode", return_value={"sub": test_user_id})
def test_service_extract_user_id_from_token(mock_jwt_decode):
    mock_request = MagicMock(spec=Request)
    mock_request.headers.get.return_value = "Bearer mock_token"
    user_id = user_service.extract_user_id_from_token(mock_request)
    mock_jwt_decode.assert_called_once_with("mock_token", options={"verify_signature": False})
    assert user_id == test_user_id


def test_service_get_dietary_criteria():
    dietary_criteria = user_service.get_dietary_criteria()
    assert Preferences.FAST_FOOD == dietary_criteria.preferences[0]
    assert Preferences.ERITREAN == dietary_criteria.preferences[-1]
    assert Restrictions.VEGETARIAN == dietary_criteria.restrictions[0]
    assert Restrictions.KOSHER == dietary_criteria.restrictions[-1]


@patch("app.logging_config.logger.error", return_value=None)
def test_validate_object_id_invalid_id(mock_logger_error):
    with pytest.raises(HTTPException) as e:
        user_service.validate_object_id("invalid_id")
    mock_logger_error.assert_called_once()
    assert e.value.status_code == 422
