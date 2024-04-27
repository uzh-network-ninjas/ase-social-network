from pymongo.results import InsertOneResult
from unittest.mock import MagicMock

REVIEW_ID = "11111"
USER_ID = "22222"
LOCATION_ID = "33333"

MOCK_REVIEW_RESPONSE_DATA_MONGODB = {
    "_id": REVIEW_ID,
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
    "liked_by": [],
    "created_at": "1999-01-01T01:01:01.123456"
}

class MockReviewRepository:

    @staticmethod
    async def add_review(review, user_id, username) -> InsertOneResult:
        insert_one_result = MagicMock(spec=InsertOneResult)
        insert_one_result.inserted_id = REVIEW_ID
        return insert_one_result

    @staticmethod
    async def get_review_by_id(review_id) -> dict:
        return MOCK_REVIEW_RESPONSE_DATA_MONGODB