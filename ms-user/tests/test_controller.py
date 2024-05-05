import pytest
from unittest.mock import patch
from datetime import datetime
from app.models.UserOut import UserOut

# Test data setup
test_user_id = "test_user_id"
test_user_id_second = "test_user_id_second"
test_username = "test_user"
test_username_second = "test_user_second"
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
test_user_second = {
    "id": test_user_id_second,
    "username": test_username_second,
    "email": "test_second@example.com",
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
    "image": f"user-images/{test_user_id}/test_image.jpg",
    "preferences": [],
    "restrictions": [],
    "following": [test_user_id_second],
    "followers": [test_user_id_second],
    "updated_at": datetime.now().isoformat()
}
test_follow = {
    "users": [test_user_second]
}
test_dietary = {
    "preferences": ["Fast Food", "Fusion"],
    "restrictions": ["Vegetarian", "Vegan"]
}


@pytest.mark.asyncio
@patch('app.UserService.UserService.validate_object_id')
@patch('app.UserService.UserService.get_user_by_id')
async def test_controller_get_user_success(mock_get_user_by_id, mock_validate_object_id, test_app):
    mock_get_user_by_id.return_value = test_user
    response = test_app.get(f"/{test_user_id}")
    assert response.status_code == 200
    assert response.json() == test_user
    mock_validate_object_id.assert_called_once()


@pytest.mark.asyncio
@patch('app.UserService.UserService.get_user_by_username')
async def test_controller_search_user_success(mock_get_user_by_username, test_app):
    mock_get_user_by_username.return_value = test_user
    response = test_app.get("/", params={
        "username": test_username
    })
    assert response.status_code == 200
    assert response.json() == test_user


@pytest.mark.asyncio
@patch('jwt.decode')  # Mock jwt.decode directly
@patch('app.UserService.UserService.update_user_by_id')
@patch('requests.patch')
async def test_controller_update_user_success(mock_request, mock_update_user_by_id, mock_jwt_decode, test_app):
    mock_jwt_decode.return_value = {"sub": test_user_id}  # Mocked user ID to be returned by jwt.decode
    mock_update_user_by_id.return_value = UserOut(**test_user_update)
    response = test_app.patch("/", json=test_user, headers=test_headers)
    assert response.status_code == 200
    assert response.json() == test_user_update
    mock_request.assert_called_once()


@pytest.mark.asyncio
@patch('jwt.decode')  # Mock jwt.decode directly
@patch('app.UserService.UserService.update_user_image_by_id')
async def test_controller_update_user_image_success(mock_update_user_image_by_id, mock_jwt_decode, test_app):
    mock_jwt_decode.return_value = {"sub": test_user_id}
    mock_update_user_image_by_id.return_value = test_user_update
    with open("/code/tests/assets/test_image.jpg", "rb") as f:
        response = test_app.patch('/image', files={"image": ("test_image.jpg", f, "image/jpeg")}, headers=test_headers)
    assert response.status_code == 200
    assert response.json() == test_user_update


@pytest.mark.asyncio
@patch('jwt.decode')
@patch('app.UserService.UserService.delete_user_by_id')
async def test_controller_delete_user_success(mock_delete_user_by_id, mock_jwt_decode, test_app):
    mock_jwt_decode.return_value = {"sub": test_user_id}
    response = test_app.delete("/", headers=test_headers)
    assert response.status_code == 204
    # Verify that the mock methods were called as expected
    mock_delete_user_by_id.assert_called_once()
    mock_jwt_decode.assert_called_once()


@pytest.mark.asyncio
@patch('app.UserService.UserService.validate_object_id')
@patch('app.UserService.UserService.get_following_users_by_id')
async def test_controller_get_following_users_success(mock_get_following_users_by_id, mock_validate_object_id, test_app):
    mock_get_following_users_by_id.return_value = test_follow
    response = test_app.get(f"/{test_user_id}/following")
    assert response.status_code == 200
    assert response.json() == test_follow
    mock_validate_object_id.assert_called_once()


@pytest.mark.asyncio
@patch('app.UserService.UserService.validate_object_id')
@patch('app.UserService.UserService.get_user_followers_by_id')
async def test_controller_get_user_followers_success(mock_get_user_followers_by_id, mock_validate_object_id, test_app):
    mock_get_user_followers_by_id.return_value = test_follow
    response = test_app.get(f"/{test_user_id}/followers")
    assert response.status_code == 200
    assert response.json() == test_follow
    mock_validate_object_id.assert_called_once()


@pytest.mark.asyncio
@patch('app.UserService.UserService.validate_object_id')
@patch('jwt.decode')
@patch('app.UserService.UserService.follow_user_by_id')
async def test_controller_follow_user_success(mock_follow_user_by_id, mock_jwt_decode, mock_validate_object_id, test_app):
    mock_jwt_decode.return_value = {"sub": test_user_id}
    mock_follow_user_by_id.return_value = test_user_update
    response = test_app.patch(f"/following/{test_user_id}", headers=test_headers)
    assert response.status_code == 200
    assert response.json() == test_user_update
    mock_validate_object_id.assert_called_once()


@pytest.mark.asyncio
@patch('app.UserService.UserService.validate_object_id')
@patch('jwt.decode')
@patch('app.UserService.UserService.unfollow_user_by_id')
async def test_controller_unfollow_user_success(mock_unfollow_user_by_id, mock_jwt_decode, mock_validate_object_id, test_app):
    mock_jwt_decode.return_value = {"sub": test_user_id}
    mock_unfollow_user_by_id.return_value = test_user
    response = test_app.delete(f"/following/{test_user_id}", headers=test_headers)
    assert response.status_code == 200
    assert response.json() == test_user
    mock_validate_object_id.assert_called_once()


@pytest.mark.asyncio
@patch('app.UserService.UserService.get_dietary_criteria')
async def test_controller_get_dietary_criteria_success(mock_get_dietary_criteria, test_app):
    mock_get_dietary_criteria.return_value = test_dietary
    response = test_app.get("/dietary_criteria/")
    assert response.status_code == 200
    assert response.json() == test_dietary
