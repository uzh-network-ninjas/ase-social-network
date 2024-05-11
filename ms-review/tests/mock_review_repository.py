from typing import List

from app.models.ReviewOut import ReviewOut
from pymongo.results import InsertOneResult, UpdateResult
from unittest.mock import MagicMock

REVIEW_ID = "11111"
USER_ID = "22222"
LOCATION_ID = "33333"
USER_NAME = "TestUser"

MOCK_REVIEW_RESPONSE_DATA_MONGODB = {
    "_id": REVIEW_ID,
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
    "liked_by": [],
    "created_at": "1999-01-01T01:01:01.123456"
}

class MockReviewRepository:

    @staticmethod
    async def add_review(review, user_id, username) -> InsertOneResult:
        insert_one_result = MagicMock(spec=InsertOneResult)
        insert_one_result.inserted_id = REVIEW_ID
        return insert_one_result

    async def update_review_by_id(self, review_id, updated_review) -> UpdateResult:
        return self._get_update_result()

    @staticmethod
    async def get_review_by_id(review_id) -> dict:
        return MOCK_REVIEW_RESPONSE_DATA_MONGODB if review_id == REVIEW_ID else {}

    @staticmethod
    async def get_feed_by_cursor_and_user_ids(timestamp_cursor, user_ids, page_size) -> List[ReviewOut]:
        return [MOCK_REVIEW_RESPONSE_DATA_MONGODB]

    @staticmethod
    async def get_reviews_by_user_id(user_id) -> List[ReviewOut]:
        return [MOCK_REVIEW_RESPONSE_DATA_MONGODB]

    @staticmethod
    async def get_reviews_by_location_and_user_ids(location_id, user_ids) -> List[ReviewOut]:
        return [MOCK_REVIEW_RESPONSE_DATA_MONGODB]

    @staticmethod
    async def get_location_ids_by_user_ids(user_ids) -> List[str]:
        return [LOCATION_ID]

    async def like_review_by_id(self, review_id, user_id) -> UpdateResult:
        return self._get_update_result()

    async def unlike_review_by_id(self, review_id, user_id) -> UpdateResult:
        return self._get_update_result()

    @staticmethod
    async def user_has_liked_review(review_id, user_id) -> bool:
        return False

    @staticmethod
    def _get_update_result() -> UpdateResult:
        update_result = MagicMock(spec=UpdateResult)
        update_result.raw_result = {"updatedExisting": True}
        return update_result