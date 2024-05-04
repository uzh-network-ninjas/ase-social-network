# MS Authenticate

The `ms-authenticate` is used for all on-boarding features such as registration, login and updating security information like the password. It is separated into its own microservice to encapsulate authentication, including JWT token generation and password hashing. However, it uses the same database as `ms-user` to enable easy access to newly added users. `ms-authenticate` provides the following endpoints:
- POST `authenticator/user`: used for registration
- POST `authenticator/token`: used for login
- PATCH `authenticator/password`: used to update the user's password