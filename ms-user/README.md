# MS User - FastAPI Microservice 👥

## Overview
The `ms-user` microservice is designed to manage all user-related activities within our application. It facilitates user profile management, including search, update, and social features like following and unfollowing users. This microservice shares its database with `ms-authenticate` to ensure seamless integration and access to user data.

## Key Features
- **User Profile Management**: Update user information such as preferences, profile pictures, and personal details.
- **Social Interactions**: Users can follow or unfollow other users, enhancing the social aspect of the application.
- **Search and Retrieval**: Retrieve user information by ID or username.

## API Endpoints
- **GET `/users/{user_id}`**: Retrieve a user by their ID.
- **GET `/users/`**: Search for a user by username with a query like `?username={username}`.
- **PATCH `/users/`**: Update the user's profile information.
- **PATCH `/users/image`**: Update the user's profile picture.
- **DELETE `/users/`**: Delete a user profile.
- **PATCH `/users/following/{user_id}`**: Follow another user.
- **DELETE `/users/following/{user_id}`**: Unfollow a user.
- **GET `/users/{user_id}/following`**: List the users that a user is following.
- **GET `/users/{user_id}/followers`**: List the users who follow the user.
- **GET `/users/dietary_criteria`**: Retrieve a list of potential dietary preferences and restrictions.

## Data Model
User profiles include the following information:
- `username`: A unique identifier chosen by the user.
- `email`: User's email address.
- `profile_picture`: A link to the user's profile image.
- `preferences`: User-selected preferences such as dietary needs.
- `restrictions`: Dietary or other restrictions.
- `following`: List of user IDs that the user is following.
- `followers`: List of user IDs that follow the user.
- All user data can be updated, except the password which is handled by `ms-authenticate`.
