import os

from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewOut import ReviewOut
from app.models.ReviewUpdate import ReviewUpdate
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult, UpdateResult
from typing import List


class ReviewRepository:
    def __init__(self):
        """
        Initializes the ReviewRepository with a MongoDB database.
        """
        client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
        db = client.ms_review_db
        self.collection = db.review_collection

    async def add_review(self, review: ReviewCreate, user_id: str, username: str) -> InsertOneResult:
        """Adds a new review to the database.

        :param review: The review data (ReviewCreate model).
        :param user_id: The ID of the user creating the review.
        :param username: The username of the user creating the review.
        :return: An InsertOneResult containing the ID of the created review.
        """
        review_dict = review.model_dump()
        review_dict["user_id"] = user_id
        review_dict["username"] = username
        review_dict["created_at"] = datetime.now()
        return await self.collection.insert_one(review_dict)

    async def update_review_by_id(self, review_id: str, updated_review: ReviewUpdate) -> UpdateResult:
        """
        Updates the specified review details in the database.

        :param review_id: The ID of the review to update.
        :param updated_review: The new details for the review (ReviewUpdate model).
        :return: The result of the update operation.
        """
        updated_reviewdata = updated_review.model_dump(exclude_unset=True)
        return await self.collection.update_one({"_id": ObjectId(review_id)}, {"$set": updated_reviewdata})

    async def get_review_by_id(self, review_id: str) -> dict:
        """Get a review by its ID.

        :param review_id: The ID of the review to retrieve.
        :return: The retrieved review.
        """
        return await self.collection.find_one({"_id": ObjectId(review_id)})

    async def get_feed_by_cursor_and_user_ids(self, timestamp_cursor: datetime, user_ids: List[str],
                                              page_size: int = 25) -> List[ReviewOut]:
        """Get a feed of reviews from the followed users.

        :param timestamp_cursor: The cursor for pagination based on timestamps.
        :param user_ids: The list of user IDs of followed users.
        :param page_size: The amount of reviews to return. Defaults to 25.
        :return: A list of reviews in the feed.
        """
        query = {
            "created_at": {"$lt": timestamp_cursor},
            "user_id": {"$in": user_ids}
        }
        return await self.collection.find(query).sort("created_at", -1).limit(page_size).to_list(length=page_size)

    async def get_reviews_by_user_id(self, user_id: str) -> List[ReviewOut]:
        """Get reviews created by a specific user.

        :param user_id: The ID of the user for the requested reviews.
        :return: A list of reviews created by the user.
        """
        return await self.collection.find({"user_id": user_id}).sort("created_at", -1).to_list(length=None)

    async def get_reviews_by_location_and_user_ids(self, location_id: str, user_ids: List[str]) -> List[ReviewOut]:
        """Get filtered reviews based on location and followed users.

        :param location_id: The ID of the location to retrieve.
        :param user_ids: The list of user IDs of followed users.
        :return: A list of filtered reviews.
        """
        query = {
            "user_id": {"$in": user_ids},
            "location.id": {"$eq": location_id}
        }
        return await self.collection.find(query).sort("created_at", -1).to_list(length=None)

    async def get_location_ids_by_user_ids(self, user_ids: List[str]) -> List[str]:
        """Get the locations for reviews of followed users.

        :param user_ids: The list of user IDs of followed users.
        :return: A list of locations for reviews of followed users.
        """
        query = {"user_id": {"$in": user_ids}}
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "$location.id"}},
            {"$project": {"location_id": "$_id", "_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        return [doc["location_id"] async for doc in cursor]

    async def like_review_by_id(self, review_id: str, user_id: str) -> UpdateResult:
        """Like a review.

        :param review_id: The ID of the review to like.
        :param user_id: The ID of the user liking a review.
        :return: An UpdateResult containing the success status.
        """
        query = {
            "$inc": {"like_count": 1},
            "$push": {"liked_by": user_id}
        }
        return await self.collection.update_one({"_id": ObjectId(review_id)}, query)

    async def unlike_review_by_id(self, review_id: str, user_id: str) -> UpdateResult:
        """Unlike a review.

        :param review_id: The ID of the review to unlike.
        :param user_id: The ID of the user unliking a review.
        :return: An UpdateResult containing the success status.
        """
        query = {
            "$inc": {"like_count": -1},
            "$pull": {"liked_by": user_id}
        }
        return await self.collection.update_one({"_id": ObjectId(review_id)}, query)

    async def user_has_liked_review(self, review_id: str, user_id: str) -> bool:
        """Checks if the user has liked the review.

        :param review_id: The ID of the review.
        :param user_id: The ID of the user.
        :return: A boolean indicating whether the user has liked the review.
        """
        query = {
            "_id": ObjectId(review_id),
            "liked_by": {"$elemMatch": {"$eq": user_id}}
        }
        return bool(await self.collection.find(query).to_list(length=None))
