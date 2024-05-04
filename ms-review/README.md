# MS Review
The `ms-review` is used for all operations on reviews in the database such as creating, filtering, feed listing and liking / unliking. The microservice uses its own database. It provides the following endpoints:
- POST `reviews/`: used to create a review
- PATCH `reviews/image`: used to add an image to a review
- GET `reviews/{review_id}`: used to get a review
- GET `reviews/feed`: used to get all reviews written by users the user is following
- GET `reviews/users`: used to get all reviews written by the user
- GET `reviews/locations`: used to get all reviews connected to a certain place
- PATCH `reviews/{review_id}/likes`: used to like a review
- DELETE `reviews/{review_id}/likes`: used to unlike a review

When a new review is created a test, the rating and the corresponding place are required. Additionally, when saving the review in the database the following fields are instantiated:
- user_id / author
- username
- image
- like_count
- liked_by
- created_at