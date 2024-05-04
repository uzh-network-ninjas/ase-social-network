# MS Authenticate

The `ms-authenticate` is used for all on-boarding features such as registration, login and updating security information like the password. It is separated into its own microservice to encapsulate authentication, including JWT token generation and password hashing. However, it uses the same database as `ms-user` to enable easy access to newly added users. `ms-authenticate` provides the following endpoints:
- POST `authenticator/user`: used for registration
- POST `authenticator/token`: used for login
- PATCH `authenticator/password`: used to update the user's password

A new user is required to provide a username, an email address and a password upon registration. The username as well as the email address must be unique. To log in a user can then use either their email address or their username in combination with their password. When saving the user in the database the following fields are instantiated:
- username
- email
- password (hashed before saved in the database)
- image / profile picture
- preferences (like `italian`)
- restrictions (like `vegan`)
- following
- followers
- created_at
- updated_at