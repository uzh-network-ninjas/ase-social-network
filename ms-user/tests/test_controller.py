import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from .main import app  # Adjust the import path according to your project structure

client = TestClient(app)

# Sample test data
test_user_id = "123"
test_username = "testuser"
test_user_data = {
    "id": test_user_id,
    "username": test_username,
    "email": "test@example.com",
    "preferences": []
}

@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_id')
async def test_get_user(mock_get_user_by_id):
    mock_get_user_by_id.return_value = test_user_data

    response = client.get(f"/{test_user_id}")
    assert response.status_code == 200
    assert response.json() == test_user_data

@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_username')
async def test_search_user(mock_get_user_by_username):
    mock_get_user_by_username.return_value = test_user_data

    response = client.get("/", params={"username": test_username})
    assert response.status_code == 200
    assert response.json() == test_user_data

@pytest.mark.asyncio
@patch('app.UserService.UserService.update_user_by_id')
async def test_update_user(mock_update_user_by_id, test_user_update_data):
    mock_update_user_by_id.return_value = test_user_update_data  # Prepare your test data for the update

    response = client.patch("/", json=test_user_update_data)
    assert response.status_code == 200
    assert response.json() == test_user_update_data

@pytest.mark.asyncio
@patch('app.UserService.UserService.delete_user_by_id')
async def test_delete_user(mock_delete_user_by_id):
    mock_delete_user_by_id.return_value = {"deleted": test_username}

    response = client.delete("/")
    assert response.status_code == 200
    assert response.json() == {"deleted": test_username}