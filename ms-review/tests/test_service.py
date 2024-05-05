import pytest

from app.models.ReviewOut import ReviewOut
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewListFilteredOut import ReviewListFilteredOut
from unittest.mock import MagicMock, patch

from fastapi import UploadFile, Request, HTTPException
from pymongo.results import UpdateResult

REVIEW_ID = "11111"
NOT_EXISTING_REVIEW_ID = "11119"
USER_ID = "22222"
LOCATION_ID = "33333"
USER_NAME = "TestUser"
IMAGE_FILENAME = "TestImage.png"

MOCK_REVIEW_DATA = {
    "text": "Great Test Place!",
    "rating": 5,
    "location": {
        "id": "testId",
        "name": "test location",
        "type": "testType",
        "coordinates": {
            "x": 1,
            "y": 1
        }
    }
}

MOCK_UPDATE_REVIEW_DATA = {
    "username": "new_username"
}

MOCK_REVIEW_RESPONSE_DATA = {
    "id": REVIEW_ID,
    "user_id": USER_ID,
    "username": USER_NAME,
    "text": "Great Test Place!",
    "rating": 5,
    "image": None,
    "location": {
        "id": LOCATION_ID,
        "name": "test location",
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

MOCK_REVIEW_LIST_FILTERED_OUT = {
    "location_reviews": [
        {
            "location_id": LOCATION_ID,
            "average_rating": 5,
            "reviews": [MOCK_REVIEW_RESPONSE_DATA]
        }
    ]
}


@pytest.mark.asyncio
async def test_create_review(review_service, test_review_create_model):
    result = await review_service.create_review(test_review_create_model(**MOCK_REVIEW_DATA), USER_ID, USER_NAME)

    assert result == ReviewOut(**MOCK_REVIEW_RESPONSE_DATA)


@pytest.mark.asyncio
@patch("boto3.client")
async def test_append_review_image_by_id(mock_boto3_client, review_service):
    mock_boto3_client.return_value = MagicMock()
    mock_image = MagicMock(spec=UploadFile)
    mock_image.filename = IMAGE_FILENAME
    mock_image.read.return_value = "mock image"

    result = await review_service.append_review_image_by_id(REVIEW_ID, mock_image, USER_ID)

    assert result == ReviewOut(**MOCK_REVIEW_RESPONSE_DATA)


@pytest.mark.asyncio
@patch("app.logging_config.logger.error", return_value=None)
@patch("boto3.client")
async def test_append_review_image_by_id_corrupt_image(mock_boto3_client, mock_logger_error, review_service):
    mock_boto3_client.return_value = MagicMock()
    mock_image = MagicMock(spec=UploadFile)

    with pytest.raises(HTTPException) as e:
        await review_service.append_review_image_by_id(REVIEW_ID, mock_image, USER_ID)
    mock_logger_error.assert_called_once()
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch("app.logging_config.logger.error", return_value=None)
@patch("boto3.client")
async def test_append_review_image_by_id_faulty_boto(mock_boto3_client, mock_logger_error, review_service):
    mock_boto3_client.return_value = None
    mock_image = MagicMock(spec=UploadFile)
    mock_image.filename = IMAGE_FILENAME
    mock_image.read.return_value = "mock image"

    with pytest.raises(HTTPException) as e:
        await review_service.append_review_image_by_id(REVIEW_ID, mock_image, USER_ID)
    mock_logger_error.assert_called_once()
    assert e.value.status_code == 400


@pytest.mark.asyncio
@patch("boto3.client")
async def test_append_review_image_by_id_update_issue(mock_boto3_client, review_service):
    mock_boto3_client.return_value = MagicMock()
    mock_image = MagicMock(spec=UploadFile)
    mock_image.filename = IMAGE_FILENAME
    mock_image.read.return_value = "mock image"

    with patch.object(review_service.review_repo, "update_review_by_id") as mock_update_review_by_id:
        update_result = MagicMock(spec=UpdateResult)
        update_result.raw_result = {"updatedExisting": False}
        mock_update_review_by_id.return_value = update_result
        with pytest.raises(HTTPException) as e:
            await review_service.append_review_image_by_id(REVIEW_ID, mock_image, USER_ID)
        assert e.value.status_code == 400


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.get_reviews_by_user_id')
async def test_service_update_review_success(mock_get_reviews_by_user_id, review_service, test_review_update_model):
    mock_get_reviews_by_user_id.return_value = ReviewListOut(**MOCK_REVIEW_LIST_RESPONSE_DATA)

    await review_service.update_review(USER_ID, test_review_update_model(**MOCK_UPDATE_REVIEW_DATA))


@pytest.mark.asyncio
@patch('app.ReviewService.ReviewService.get_reviews_by_user_id')
async def test_service_update_review_update_issue(mock_get_reviews_by_user_id, review_service,
                                                  test_review_update_model):
    mock_get_reviews_by_user_id.return_value = ReviewListOut(**MOCK_REVIEW_LIST_RESPONSE_DATA)

    with patch.object(review_service.review_repo, "update_review_by_id") as mock_update_review_by_id:
        update_result = MagicMock(spec=UpdateResult)
        update_result.raw_result = {"updatedExisting": False}
        mock_update_review_by_id.return_value = update_result
        with pytest.raises(HTTPException) as e:
            await review_service.update_review(USER_ID, test_review_update_model(**MOCK_UPDATE_REVIEW_DATA))
        assert e.value.status_code == 400


@pytest.mark.asyncio
async def test_get_review_by_id(review_service):
    result = await review_service.get_review_by_id(REVIEW_ID, USER_ID)

    assert result == ReviewOut(**MOCK_REVIEW_RESPONSE_DATA)


@pytest.mark.asyncio
async def test_get_review_by_id_not_existing(review_service):
    with pytest.raises(HTTPException) as e:
        await review_service.get_review_by_id(NOT_EXISTING_REVIEW_ID, USER_ID)
    assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_get_feed_by_cursor(review_service):
    result = await review_service.get_feed_by_cursor(None, [USER_ID], USER_ID)

    assert result == ReviewListOut(**MOCK_REVIEW_LIST_RESPONSE_DATA)


@pytest.mark.asyncio
async def test_get_feed_by_cursor_no_followings(review_service):
    with pytest.raises(HTTPException) as e:
        await review_service.get_feed_by_cursor(None, [], USER_ID)
    assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_get_feed_by_cursor_no_reviews(review_service):
    with patch.object(review_service.review_repo, "get_feed_by_cursor_and_user_ids") as mock_get_feed:
        mock_get_feed.return_value = []
        with pytest.raises(HTTPException) as e:
            await review_service.get_feed_by_cursor(None, [USER_ID], USER_ID)
        assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews_by_user_id(review_service):
    result = await review_service.get_reviews_by_user_id(USER_ID, USER_ID)

    assert result == ReviewListOut(**MOCK_REVIEW_LIST_RESPONSE_DATA)


@pytest.mark.asyncio
async def test_get_reviews_by_user_id_no_reviews(review_service):
    with patch.object(review_service.review_repo, "get_reviews_by_user_id") as mock_get_reviews:
        mock_get_reviews.return_value = []
        with pytest.raises(HTTPException) as e:
            await review_service.get_reviews_by_user_id(USER_ID, USER_ID)
        assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews_by_locations(review_service):
    result = await review_service.get_reviews_by_locations([LOCATION_ID], [USER_ID], USER_ID)

    assert result == ReviewListFilteredOut(**MOCK_REVIEW_LIST_FILTERED_OUT)


@pytest.mark.asyncio
async def test_get_reviews_by_locations_no_filter(review_service):
    result = await review_service.get_reviews_by_locations(None, [USER_ID], USER_ID)

    assert result == ReviewListFilteredOut(**MOCK_REVIEW_LIST_FILTERED_OUT)


@pytest.mark.asyncio
async def test_get_reviews_by_locations_no_followings(review_service):
    with pytest.raises(HTTPException) as e:
        await review_service.get_reviews_by_locations(None, [], USER_ID)
    assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews_by_locations_no_reviews(review_service):
    with patch.object(review_service.review_repo, "get_location_ids_by_user_ids") as mock_get_locations:
        mock_get_locations.return_value = []
        with pytest.raises(HTTPException) as e:
            await review_service.get_reviews_by_locations(None, [USER_ID], USER_ID)
        assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews_by_locations_bad_combination(review_service):
    with patch.object(review_service.review_repo, "get_reviews_by_location_and_user_ids") as mock_get_reviews:
        mock_get_reviews.return_value = []
        with pytest.raises(HTTPException) as e:
            await review_service.get_reviews_by_locations(None, [USER_ID], USER_ID)
        assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_like_review_by_id(review_service):
    result = await review_service.like_review_by_id(REVIEW_ID, USER_ID)

    assert result == ReviewOut(**MOCK_REVIEW_RESPONSE_DATA)


@pytest.mark.asyncio
async def test_like_review_by_id_not_existing(review_service):
    with pytest.raises(HTTPException) as e:
        await review_service.like_review_by_id(NOT_EXISTING_REVIEW_ID, USER_ID)
    assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_like_review_by_id_has_liked(review_service):
    with patch.object(review_service.review_repo, "user_has_liked_review") as mock_user_has_liked_review:
        mock_user_has_liked_review.return_value = True
        with pytest.raises(HTTPException) as e:
            await review_service.like_review_by_id(REVIEW_ID, USER_ID)
        assert e.value.status_code == 400


@pytest.mark.asyncio
async def test_like_review_by_id_update_issue(review_service):
    with patch.object(review_service.review_repo, "like_review_by_id") as mock_like_review:
        update_result = MagicMock(spec=UpdateResult)
        update_result.raw_result = {"updatedExisting": False}
        mock_like_review.return_value = update_result
        with pytest.raises(HTTPException) as e:
            await review_service.like_review_by_id(REVIEW_ID, USER_ID)
        assert e.value.status_code == 400


@pytest.mark.asyncio
async def test_unlike_review_by_id(review_service):
    with patch.object(review_service.review_repo, "user_has_liked_review") as mock_user_has_liked_review:
        mock_user_has_liked_review.return_value = True
        result = await review_service.unlike_review_by_id(REVIEW_ID, USER_ID)

    assert result == ReviewOut(**MOCK_REVIEW_RESPONSE_DATA)


@pytest.mark.asyncio
async def test_unlike_review_by_id_not_existing(review_service):
    with pytest.raises(HTTPException) as e:
        await review_service.unlike_review_by_id(NOT_EXISTING_REVIEW_ID, USER_ID)
    assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_unlike_review_by_id_has_unliked(review_service):
    with patch.object(review_service.review_repo, "user_has_liked_review") as mock_user_has_liked_review:
        mock_user_has_liked_review.return_value = False
        with pytest.raises(HTTPException) as e:
            await review_service.unlike_review_by_id(REVIEW_ID, USER_ID)
        assert e.value.status_code == 400


@pytest.mark.asyncio
async def test_unlike_review_by_id_update_issue(review_service):
    with patch.object(review_service.review_repo, "user_has_liked_review") as mock_user_has_liked_review:
        mock_user_has_liked_review.return_value = True
        with patch.object(review_service.review_repo, "unlike_review_by_id") as mock_unlike_review:
            update_result = MagicMock(spec=UpdateResult)
            update_result.raw_result = {"updatedExisting": False}
            mock_unlike_review.return_value = update_result
            with pytest.raises(HTTPException) as e:
                await review_service.unlike_review_by_id(REVIEW_ID, USER_ID)
            assert e.value.status_code == 400


@patch("app.ReviewService.ReviewService.extract_payload_from_token", return_value={"sub": USER_ID})
def test_extract_user_id_from_token(mock_extract_payload, review_service):
    mock_request = MagicMock(spec=Request)

    user_id = review_service.extract_user_id_from_token(mock_request)

    mock_extract_payload.assert_called_once_with(mock_request)
    assert user_id == USER_ID


@patch("app.ReviewService.ReviewService.extract_payload_from_token", return_value={"username": USER_NAME})
def test_extract_username_from_token(mock_extract_payload, review_service):
    mock_request = MagicMock(spec=Request)

    user_name = review_service.extract_username_from_token(mock_request)

    mock_extract_payload.assert_called_once_with(mock_request)
    assert user_name == USER_NAME


@patch("jwt.decode", return_value={"sub": USER_ID, "username": USER_NAME})
def test_extract_payload_from_token(mock_jwt_decode, review_service):
    mock_request = MagicMock(spec=Request)
    mock_request.headers.get.return_value = "Bearer test_token"

    payload = review_service.extract_payload_from_token(mock_request)

    mock_jwt_decode.assert_called_once_with("test_token", options={"verify_signature": False})
    assert payload == {"sub": USER_ID, "username": USER_NAME}


@patch("app.logging_config.logger.error", return_value=None)
def test_validate_object_id_invalid_id(mock_logger_error, review_service):
    with pytest.raises(HTTPException) as e:
        review_service.validate_object_id("invalid_id")
    mock_logger_error.assert_called_once()
    assert e.value.status_code == 422
