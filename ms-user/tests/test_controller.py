import pytest
from unittest.mock import patch
from datetime import datetime

# Test data setup
test_user_id = "test_user_id"
test_username = "test_user"
test_headers = {"Authorization": "Bearer mock_token"}
test_user = {
    "id": test_user_id,
    "username": test_username,
    "email": "test@example.com",
    "created_at": datetime.now().isoformat(),
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
    "created_at": datetime.now().isoformat(),
    "image": None,
    "preferences": [],
    "restrictions": [],
    "following": [],
    "followers": [],
    "updated_at": datetime.now().isoformat()
}


@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_id')
async def test_controller_get_user_success(mock_get_user_by_id, test_app):  # Now using the test_app fixture
    mock_get_user_by_id.return_value = test_user
    response = test_app.get(f"/{test_user_id}")
    assert response.status_code == 200
    assert response.json() == test_user


@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_username')
async def test_controller_search_user_success(mock_get_user_by_username, test_app):  # test_app fixture injected
    mock_get_user_by_username.return_value = test_user
    response = test_app.get("/", params={
        "username": test_username
    })
    assert response.status_code == 200
    assert response.json() == test_user


@pytest.mark.asyncio
@patch('jwt.decode')  # Mock jwt.decode directly
@patch('app.UserService.UserService.update_user_by_id')
async def test_controller_update_user_success(mock_update_user_by_id, mock_jwt_decode, test_app):  # test_app used
    mock_jwt_decode.return_value = {"sub": test_user_id}  # Mocked user ID to be returned by jwt.decode
    mock_update_user_by_id.return_value = test_user_update  # Adjust based on actual test update data
    response = test_app.patch("/", json=test_user, headers=test_headers)  # Make sure this matches the structure of your update payload
    assert response.status_code == 200
    assert response.json() == test_user_update


@pytest.mark.asyncio
@patch('jwt.decode')  # Mock jwt.decode directly
@patch('app.UserService.UserService.delete_user_by_id')
async def test_controller_delete_user_success(mock_delete_user_by_id, mock_jwt_decode, test_app):
    mock_jwt_decode.return_value = {"sub": test_user_id}  # Mocked user ID to be returned by jwt.decode
    # Perform the delete request with the Authorization header
    response = test_app.delete("/", headers=test_headers)
    # Assertions
    assert response.status_code == 204
    # Verify that the mock methods were called as expected
    mock_delete_user_by_id.assert_called_once()
    mock_jwt_decode.assert_called_once()
