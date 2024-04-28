import pytest
from unittest.mock import MagicMock, patch
from app.AuthenticateService import AuthenticateService
from app.models.UserRegister import UserRegister
from app.models.UserLogin import UserLogin
from app.models.UpdateUserPassword import UpdateUserPassword
from fastapi import HTTPException, Request

test_user = {
    "id": "test_user_id",
    "username": "test_user",
    "email": "test_user@example.com",
    "password": "test_password"
}

auth_service = AuthenticateService()
hashed_user = {
    "id": "test_user_id",
    "username": "test_user",
    "email": "test_user@example.com",
    "password": auth_service.auth_encryption['pwd_context'].hash("test_password")
}

dummy_request = Request({
    "type": "http",
    "method": "PATCH",
    "url": "http://testserver/",
    "headers": {},
})


@patch("jwt.decode", return_value={"sub": "test_user_id"})
def test_service_extract_user_id(mock_jwt_decode):
    mock_request = MagicMock(spec=Request)
    mock_request.headers.get.return_value = "Bearer mock_token"
    user_id = auth_service.extract_user_id(mock_request)
    mock_jwt_decode.assert_called_once_with("mock_token", options={"verify_signature": False})
    assert user_id == "test_user_id"


@pytest.mark.asyncio
@patch('app.AuthenticateRepository.AuthenticateRepository.username_exists')
@patch('app.AuthenticateRepository.AuthenticateRepository.user_email_exists')
@patch('app.AuthenticateRepository.AuthenticateRepository.add_user')
async def test_service_user_registration_success(mock_add_user, mock_user_email_exists, mock_username_exists):
    mock_username_exists.return_value = False
    mock_user_email_exists.return_value = False
    mock_add_user.return_value = UserLogin(**test_user)
    registered_user = await auth_service.register_user(UserRegister(**test_user))
    assert test_user.get('username') == registered_user.username
    assert test_user.get('email') == registered_user.email
    assert test_user.get('password') == registered_user.password


@pytest.mark.asyncio
@patch('app.AuthenticateRepository.AuthenticateRepository.username_exists')
async def test_service_user_registration_username_already_exists(mock_username_exists):
    mock_username_exists.return_value = True
    with pytest.raises(HTTPException) as e:
        await auth_service.register_user(UserRegister(**test_user))
    assert e.value.status_code == 409


@pytest.mark.asyncio
@patch('app.AuthenticateRepository.AuthenticateRepository.username_exists')
@patch('app.AuthenticateRepository.AuthenticateRepository.user_email_exists')
async def test_service_user_registration_user_email_already_exists(mock_user_email_exists, mock_username_exists):
    mock_username_exists.return_value = False
    mock_user_email_exists.return_value = True
    with pytest.raises(HTTPException) as e:
        await auth_service.register_user(UserRegister(**test_user))
    assert e.value.status_code == 409


@pytest.mark.asyncio
@patch('app.AuthenticateRepository.AuthenticateRepository.user_exists')
@patch('app.AuthenticateRepository.AuthenticateRepository.get_user_by_name_or_email')
async def test_service_user_login_username_success(mock_get_user_by_name_or_email, mock_user_exists):
    mock_user_exists.return_value = True
    mock_get_user_by_name_or_email.return_value = UserLogin(**hashed_user)
    curr_user = {
        "username": "test_user",
        "password": "test_password"
    }
    token = await auth_service.login_user(UserLogin(**curr_user))
    assert token


@pytest.mark.asyncio
@patch('app.AuthenticateRepository.AuthenticateRepository.user_exists')
@patch('app.AuthenticateRepository.AuthenticateRepository.get_user_by_name_or_email')
async def test_service_user_login_email_success(mock_get_user_by_name_or_email, mock_user_exists):
    mock_user_exists.return_value = True
    mock_get_user_by_name_or_email.return_value = UserLogin(**hashed_user)
    curr_user = {
        "email": "test_user@example.com",
        "password": "test_password"
    }
    token = await auth_service.login_user(UserLogin(**curr_user))
    assert token


@pytest.mark.asyncio
@patch('app.AuthenticateRepository.AuthenticateRepository.user_exists')
async def test_service_user_login_user_does_not_exist(mock_user_exists):
    mock_user_exists.return_value = False
    with pytest.raises(HTTPException) as e:
        await auth_service.login_user(UserLogin(**test_user))
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch('app.AuthenticateRepository.AuthenticateRepository.user_exists')
@patch('app.AuthenticateRepository.AuthenticateRepository.get_user_by_name_or_email')
async def test_service_user_login_wrong_password(mock_get_user_by_name_or_email, mock_user_exists):
    mock_user_exists.return_value = True
    mock_get_user_by_name_or_email.return_value = UserLogin(**hashed_user)
    curr_user = {
        "email": "test_user@example.com",
        "password": "wrong_test_password"
    }
    with pytest.raises(HTTPException) as e:
        await auth_service.login_user(UserLogin(**curr_user))
    assert e.value.status_code == 401


@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.extract_user_id')
@patch('app.AuthenticateRepository.AuthenticateRepository.get_user_by_id')
@patch('app.AuthenticateRepository.AuthenticateRepository.update_user_password')
async def test_service_update_user_password_success(mock_update_user_password, mock_get_user_by_id, mock_extract_user_id):
    mock_get_user_by_id.return_value = UserLogin(**hashed_user)
    mock_extract_user_id.return_value = "test_user_id"
    curr_update_password = {
        "curr_password": "test_password",
        "new_password": "new_test_password"
    }
    await auth_service.update_user_password(dummy_request, UpdateUserPassword(**curr_update_password))
    mock_update_user_password.assert_called_once()


@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.extract_user_id')
@patch('app.AuthenticateRepository.AuthenticateRepository.get_user_by_id')
async def test_service_update_user_password_wrong_password(mock_get_user_by_id, mock_extract_user_id):
    mock_get_user_by_id.return_value = UserLogin(**hashed_user)
    mock_extract_user_id.return_value = "test_user_id"
    curr_update_password = {
        "curr_password": "wrong_test_password",
        "new_password": "new_test_password"
    }
    with pytest.raises(HTTPException) as e:
        await auth_service.update_user_password(dummy_request, UpdateUserPassword(**curr_update_password))
    assert e.value.status_code == 401


@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.extract_user_id')
@patch('app.AuthenticateRepository.AuthenticateRepository.get_user_by_id')
async def test_service_update_user_password_same_password(mock_get_user_by_id, mock_extract_user_id):
    mock_get_user_by_id.return_value = UserLogin(**hashed_user)
    mock_extract_user_id.return_value = "test_user_id"
    curr_update_password = {
        "curr_password": "test_password",
        "new_password": "test_password"
    }
    with pytest.raises(HTTPException) as e:
        await auth_service.update_user_password(dummy_request, UpdateUserPassword(**curr_update_password))
    assert e.value.status_code == 400
