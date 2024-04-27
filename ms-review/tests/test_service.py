import pytest

from app.models.ReviewOut import ReviewOut

REVIEW_ID = "11111"
USER_ID = "22222"
LOCATION_ID = "33333"
USER_NAME = "TestUser"

MOCK_REVIEW_DATA = {
    "text": "This is a test review!",
    "rating": 5,
    "location": {
        "id": "testId",
        "name": "testlocation",
        "type": "testType",
        "coordinates": {
            "x": 1,
            "y": 1
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

@pytest.mark.asyncio
async def test_create_review(review_service, test_review_create_model):
    result = await review_service.create_review(test_review_create_model(**MOCK_REVIEW_DATA), USER_ID, USER_NAME)

    assert result == ReviewOut(**MOCK_REVIEW_RESPONSE_DATA)




# @pytest.mark.asyncio
# # @patch('app.ReviewRepository.ReviewRepository.add_review', return_value="")
# # @patch('app.ReviewRepository.ReviewRepository.get_review_by_id', return_value="")
# async def test_create_review_old(review_service, test_review_create_model):
#     review = test_review_create_model(**review_data)
#     review_service.rr.add_review = MagicMock(return_value=MagicMock(inserted_id="mocked_review_id"))
#     review_service.get_review_by_id = MagicMock(return_value=MagicMock())
#
#     result = await review_service.create_review(review, USER_ID, USER_NAME)
#
#     assert result is not None
#     review_service.rr.add_review.assert_called_once_with(review, USER_ID, USER_NAME)
#     review_service.get_review_by_id.assert_called_once_with("mocked_review_id", USER_ID)