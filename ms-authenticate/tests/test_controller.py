import pytest
from unittest.mock import patch

# Assuming test_user_data is a dictionary that represents the user data you expect to return
test_user = {
    "id": "test_user_id",
    "username": "test_user",
    "email": "test_user@example.com",
    "password": "test_password"
}
test_access_token = "test_access_token"


@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.register_user')
@patch('app.AuthenticateService.AuthenticateService.login_user')
async def test_controller_user_registration_success(mock_login_user, mock_register_user,  test_app):
    # Configure the mock to return your test user data when called
    mock_register_user.return_value = test_user
    mock_login_user.return_value = test_access_token
    # Perform the test registration request
    response = test_app.post("/user", json={
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "test_password"
    })
    assert response.status_code == 201
    assert response.json() == {"access_token": test_access_token, "token_type": "bearer"}


@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.login_user')
async def test_controller_user_login_success(mock_login_user, test_app):
    # Configure the mock to return your fake token response when called
    mock_login_user.return_value = test_access_token
    # Perform the test login request
    response = test_app.post("/token", json={
        "username": "test_user",
        "password": "test_password"
    })
    assert response.status_code == 201
    assert response.json() == {"access_token": test_access_token, "token_type": "bearer"}


@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.update_user_password')
async def test_controller_update_user_password_success(mock_update_user_password, test_app):
    response = test_app.patch("/password", json={
        "curr_password": "test_password",
        "new_password": "new_test_password"
    })
    assert response.status_code == 204
    mock_update_user_password.assert_called_once()
