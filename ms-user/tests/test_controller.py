import pytest
from unittest.mock import AsyncMock, patch

# Test data setup
test_user_id = "123"
test_username = "testuser"
test_user_data = {
    "id": test_user_id,
    "username": test_username,
    "email": "test@example.com",
    "preferences": []
}

test_user_data_update = {
    "username": test_username,
    "email": "test@example.com",
    "preferences": []
}

@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_id')
async def test_get_user(mock_get_user_by_id, test_app):  # Now using the test_app fixture
    mock_get_user_by_id.return_value = test_user_data

    response = test_app.get(f"/{test_user_id}")
    assert response.status_code == 200
    assert response.json() == test_user_data

@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_username')
async def test_search_user(mock_get_user_by_username, test_app):  # test_app fixture injected
    mock_get_user_by_username.return_value = test_user_data

    response = test_app.get("/", params={"username": test_username})
    assert response.status_code == 200
    assert response.json() == test_user_data

@pytest.mark.asyncio
@patch('jwt.decode')  # Mock jwt.decode directly
@patch('app.UserService.UserService.update_user_by_id')
async def test_update_user(mock_update_user_by_id, mock_jwt_decode,test_app):  # test_app used
    mock_jwt_decode.return_value = {"sub": "123"}  # Mocked user ID to be returned by jwt.decode
    
    mock_update_user_by_id.return_value = test_user_data  # Adjust based on actual test update data

    headers = {"Authorization": "Bearer mocktoken"}
    response = test_app.patch("/", json=test_user_data, headers=headers)  # Make sure this matches the structure of your update payload
    print(test_user_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == test_user_data_update

    

@pytest.mark.asyncio
@patch('jwt.decode')  # Mock jwt.decode directly
@patch('app.UserService.UserService.delete_user_by_id')
async def test_delete_user(mock_delete_user_by_id, mock_jwt_decode, test_app):
    # Set up the mock return value for the jwt.decode call
    mock_jwt_decode.return_value = {"sub": "123"}  # Mocked user ID to be returned by jwt.decode
    mock_delete_user_by_id.return_value = {"deleted": "test_username"}
    headers = {"Authorization": "Bearer mocktoken"}

    # Perform the delete request with the Authorization header
    response = test_app.delete("/", headers=headers)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"deleted": "test_username"}

    # Verify that the mock methods were called as expected
    mock_delete_user_by_id.assert_called_once()
    mock_jwt_decode.assert_called_once()