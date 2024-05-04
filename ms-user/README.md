# MS User
The `ms-user` is used for all operations on users in the database such as searching, adding information and follow / unfollow users. The microservice uses the same database as `ms-authenticate` to enable easy access to newly added users and their IDs. It provides the following endpoints:
- GET `users/{user_id}`: used to get a user by ID
- GET `users/?username={username}`: used to get a user by username
- PATCH `users/`: used to update the user's profile (for example with preferences, username, email)
- PATCH `users/image`: used to update the user's profile picture
- DELETE `users/`: used to delete the user
- PATCH `users/following/{user_id}`: used to follow another user
- DELETE `users/following/{user_id}`: used to unfollow another user
- GET `users/{user_id}/following`: used to get a list of users the user is following
- GET `users/{user_id}/followers`: used to get a list of users who follow the user
- GET `users/dietary_criteria`: used to get a list of possible preferences and restrictions

Upon log in the user is able to change their data including username, email, profile picture, preferences and restrictions. The password is changed via `ms-authenticate` to separate responsibility.