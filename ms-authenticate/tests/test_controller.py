import pytest
from unittest.mock import patch
from datetime import datetime

# Assuming test_user_data is a dictionary that represents the user data you expect to return
test_user_data = {
    "id": "unique_user_id",
    "username": "testuser",
    "email": "testuser@example.com",
    "created_at": datetime.now().isoformat(),
    "updated_at": None
}
access_token = "fake_token123"

@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.register_user')
@patch('app.AuthenticateService.AuthenticateService.login_user')
async def test_user_registration(mock_login_user, mock_register_user,  test_app):
    # Configure the mock to return your test user data when called
    mock_register_user.return_value = test_user_data
    mock_login_user.return_value = access_token

    # Perform the test registration request
    response = test_app.post("/user", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "strongpassword123",
        "preferences": ["pref1", "pref2"],
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    })

    # assert response.status_code == 201
    # assert response.json() == test_user_data
    assert response.status_code == 201
    assert response.json() == {"access_token": access_token, "token_type": "bearer"}


@pytest.mark.asyncio
@patch('app.AuthenticateService.AuthenticateService.login_user')
async def test_user_login(mock_login_user, test_app):
    # Configure the mock to return your fake token response when called
    mock_login_user.return_value = access_token

    # Perform the test login request
    response = test_app.post("/token", json={
        "username": "testuser",
        "password": "strongpassword123"
    })

    assert response.status_code == 201
    assert response.json() == {"access_token": access_token, "token_type": "bearer"}