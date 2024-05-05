import pytest
from unittest.mock import patch, MagicMock

REVIEW_ID = "11111"
USER_ID = "22222"
LOCATION_ID = "33333"

MOCK_REVIEW_DATA = {
    "text": "Great Test Place!",
    "rating": 5,
    "location": {
        "id": LOCATION_ID,
        "name": "Test Location",
        "type": "testType",
        "coordinates": {
            "x": 1.00,
            "y": 1.00
        }
    }
}

MOCK_REVIEW_RESPONSE_DATA = {
    "id": REVIEW_ID,
    "user_id": USER_ID,
    "username": "TestImage.png",
    "text": "Great Test Place!",
    "rating": 5,
    "image": None,
    "location": {
        "id": LOCATION_ID,
        "name": "Test Location",
        "type": "testType",
        "coordinates": {
            "x": 1.00,
            "y": 1.00
        }
    },
    "like_count": 0,
    "liked_by_current_user": False,
    "created_at": "1999-01-01T01:01:01.123456"
}

MOCK_REVIEW_LIST_RESPONSE_DATA = {
    "reviews": [MOCK_REVIEW_RESPONSE_DATA]
}

MOCK_REVIEW_LIST_FILTERED_RESPONSE_DATA = {
    "location_reviews": [
        {
            "location_id": LOCATION_ID,
            "average_rating": 2,
            "reviews": [MOCK_REVIEW_RESPONSE_DATA]
        }
    ]
}


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('app.ReviewService.ReviewService.extract_username_from_token', return_value="TestUser")
@patch('app.ReviewService.ReviewService.create_review', return_value=MOCK_REVIEW_RESPONSE_DATA)
async def test_create_review(mock_create_review, mock_extract_username, mock_extract_user_id, test_app,
                             test_review_out_model):
    response = test_app.post('/', json=MOCK_REVIEW_DATA)

    mock_create_review.assert_called_once()
    mock_extract_username.assert_called_once()
    mock_extract_user_id.assert_called_once()
    assert response.status_code == 201
    assert response.json() == MOCK_REVIEW_RESPONSE_DATA
    assert test_review_out_model(**response.json())


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.validate_object_id', return_value=None)
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('app.ReviewService.ReviewService.append_review_image_by_id', return_value=MOCK_REVIEW_RESPONSE_DATA)
async def test_append_review_image(mock_append_review_image, mock_extract_user_id, mock_validate_object_id, test_app,
                                   test_review_out_model):
    with open("/code/tests/assets/test_image.jpg", "rb") as f:
        response = test_app.patch('/image', data={"review_id": REVIEW_ID},
                                  files={"image": ("test_image.jpg", f, "image/jpeg")})

    mock_append_review_image.assert_called_once()
    mock_extract_user_id.assert_called_once()
    mock_validate_object_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == MOCK_REVIEW_RESPONSE_DATA
    assert test_review_out_model(**response.json())


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('app.ReviewService.ReviewService.update_review')
async def test_controller_update_review_success(mock_update_review, mock_extract_user_id_from_token, test_app):
    response = test_app.patch("/", json={
        "username": "new_username"
    })
    assert response.status_code == 204
    mock_extract_user_id_from_token.assert_called_once()
    mock_update_review.assert_called_once()


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.validate_object_id', return_value=None)
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('app.ReviewService.ReviewService.get_review_by_id', return_value=MOCK_REVIEW_RESPONSE_DATA)
async def test_get_review(mock_get_review, mock_extract_user_id, mock_validate_object_id, test_app,
                          test_review_out_model):
    response = test_app.get(f"/{REVIEW_ID}")

    mock_get_review.assert_called_once_with(REVIEW_ID, USER_ID)
    mock_extract_user_id.assert_called_once()
    mock_validate_object_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == MOCK_REVIEW_RESPONSE_DATA
    assert test_review_out_model(**response.json())


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('requests.get')
@patch('app.ReviewService.ReviewService.get_feed_by_cursor', return_value=MOCK_REVIEW_LIST_RESPONSE_DATA)
async def test_get_feed(mock_get_feed, mock_request, mock_extract_user_id, test_app, test_review_list_out_model):
    mock_response = MagicMock()
    mock_response.json.return_value = {"following": []}
    mock_request.return_value = mock_response

    response = test_app.get("/")

    mock_get_feed.assert_called_once_with(None, [], USER_ID)
    mock_request.assert_called_once()
    mock_extract_user_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == MOCK_REVIEW_LIST_RESPONSE_DATA
    assert test_review_list_out_model(**response.json())


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.validate_object_id', return_value=None)
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('app.ReviewService.ReviewService.get_reviews_by_user_id', return_value=MOCK_REVIEW_LIST_RESPONSE_DATA)
async def test_get_reviews_from_user(mock_get_reviews, mock_extract_user_id, mock_validate_object_id, test_app,
                                     test_review_list_out_model):
    response = test_app.get("/users/?user_id=22221")

    mock_get_reviews.assert_called_once_with("22221", USER_ID)
    mock_extract_user_id.assert_called_once()
    mock_validate_object_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == MOCK_REVIEW_LIST_RESPONSE_DATA
    assert test_review_list_out_model(**response.json())


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('requests.get')
@patch('app.ReviewService.ReviewService.get_reviews_by_locations', return_value=MOCK_REVIEW_LIST_FILTERED_RESPONSE_DATA)
async def test_get_filtered_reviews(mock_get_reviews, mock_requests_get, mock_extract_user_id, test_app,
                                    test_review_list_filtered_out_model):
    mock_requests_get.return_value.json.return_value = {"following": [22221]}

    response = test_app.get("/locations/")

    mock_get_reviews.assert_called_once_with(None, [22221], USER_ID)
    mock_requests_get.assert_called_once()
    mock_extract_user_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == MOCK_REVIEW_LIST_FILTERED_RESPONSE_DATA
    assert test_review_list_filtered_out_model(**response.json())


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.validate_object_id', return_value=None)
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('app.ReviewService.ReviewService.like_review_by_id', return_value=MOCK_REVIEW_RESPONSE_DATA)
async def test_like_review(mock_like_review, mock_extract_user_id, mock_validate_object_id, test_app,
                           test_review_out_model):
    response = test_app.patch(f"/{REVIEW_ID}/likes")

    mock_like_review.assert_called_once_with(REVIEW_ID, USER_ID)
    mock_extract_user_id.assert_called_once()
    mock_validate_object_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == MOCK_REVIEW_RESPONSE_DATA
    assert test_review_out_model(**response.json())


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.validate_object_id', return_value=None)
@patch('app.ReviewService.ReviewService.extract_user_id_from_token', return_value=USER_ID)
@patch('app.ReviewService.ReviewService.unlike_review_by_id', return_value=MOCK_REVIEW_RESPONSE_DATA)
async def test_unlike_review(mock_unlike_review, mock_extract_user_id, mock_validate_object_id, test_app,
                             test_review_out_model):
    response = test_app.delete(f"/{REVIEW_ID}/likes")

    mock_unlike_review.assert_called_once_with(REVIEW_ID, USER_ID)
    mock_extract_user_id.assert_called_once()
    mock_validate_object_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == MOCK_REVIEW_RESPONSE_DATA
    assert test_review_out_model(**response.json())
