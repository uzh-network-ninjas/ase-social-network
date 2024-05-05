# MS Review - FastAPI Microservice 🌟
## Overview
The `ms-review` microservice manages all review-related functionalities within our application. It handles operations such as creating, updating, and querying reviews, and operates with its own dedicated database to maintain independence and performance.

## Key Features
- **Create Reviews**: Users can submit reviews, which include text, ratings, and optionally images.
- **Review Interactions**: Users can like or unlike reviews.
- **Query Reviews**: Supports filtering reviews by various criteria, including author and location.

## API Endpoints
- **POST `/reviews/`**: Create a new review.
- **PATCH `/reviews/image`**: Add an image to an existing review.
- **GET `/reviews/{review_id}`**: Retrieve a specific review.
- **GET `/reviews/feed`**: Fetch all reviews from users the requesting user follows.
- **GET `/reviews/users`**: Obtain all reviews written by the requesting user.
- **GET `/reviews/locations`**: Retrieve reviews linked to a specific location.
- **PATCH `/reviews/{review_id}/likes`**: Like a specific review.
- **DELETE `/reviews/{review_id}/likes`**: Unlike a review.

## Data Model
When a new review is created a test, the rating and the corresponding place are required. Additionally, when saving the review in the database the following fields are instantiated:
- `user_id / author`: The ID of the user who wrote the review.
- `username`: The username of the author.
- `image`: An optional image added to the review.
- `like_count`: The number of likes the review has received.
- `liked_by`: A list of users who have liked the review.
- `created_at`: The timestamp when the review was created.