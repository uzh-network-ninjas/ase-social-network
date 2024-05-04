# MS Authenticate - FastAPI Microservice 🛡️

## Overview
The `ms-authenticate` microservice is crucial for handling all onboarding functionalities such as user registration, login, and updating security features like password management. It plays a key role in user authentication, generating JWT tokens, and securing password hashes.

It shares a database with `ms-user` to ensure seamless integration and immediate access to user data post-registration.

## Key Features
- **User Registration**: Register with username, email, and password.
- **User Login**: Authenticate using username or email and password.
- **Password Management**: Securely update user passwords.

## API Endpoints
- **POST `/authenticator/user`**: Registers a new user.
- **POST `/authenticator/token`**: Generates a token upon login.
- **PATCH `/authenticator/password`**: Updates a user's password.

## Data Model
Upon registration, the following details are stored:
- `username`: Must be unique.
- `email`: Must be unique and used for logging in.
- `password`: Hashed for security.
- `image`: Profile picture or avatar.
- `preferences`: Such as 'Italian cuisine'.
- `restrictions`: Such as 'vegan'.
- `following`: List of followed users.
- `followers`: List of followers.
- `created_at`: Account creation timestamp.
- `updated_at`: Last update timestamp.

## Technology Stack
- **FastAPI**: For high performance and easy API creation.
- **JWT**: For secure token generation.
- **Bcrypt**: For password hashing