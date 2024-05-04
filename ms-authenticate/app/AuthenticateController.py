from fastapi import FastAPI, status, Request
from app.AuthenticateService import AuthenticateService
from app.models.UserLogin import UserLogin
from app.models.UserRegister import UserRegister
from app.models.UpdateUserPassword import UpdateUserPassword
import os

app = FastAPI()
auth_service = AuthenticateService()


def check_env_vars():
    """
    Checks for the presence of required environment variables in the system's environment settings.

    :raises EnvironmentError: If any required environment variables are missing, they are listed.
    """
    required_env_vars = ["MONGO_URL", "JWT_KONG_KEY", "JWT_SECRET", "JWT_ALGORITHM"]
    missing_vars = [var for var in required_env_vars if var not in os.environ]
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")


check_env_vars()


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister) -> dict[str, str]:
    """
    Registers a new user in the system and generates a JWT access token.

    :param user: The user data (UserRegister model).
    :return: A dictionary containing the JWT access token and token type.
    """
    registered_user = await auth_service.register_user(user)
    access_token = await auth_service.login_user(registered_user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token", status_code=status.HTTP_201_CREATED)
async def login_generate_token(user: UserLogin) -> dict[str, str]:
    """
    Authenticates an existing user and generates a JWT access token.

    :param user: The user data (UserLogin model).
    :return: A dictionary containing the JWT access token and token type.
    """
    access_token = await auth_service.login_user(user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(request: Request, update_user_password: UpdateUserPassword):
    """
    Changes the user's current password to the new one.

    :param request: The request object (provided by FastAPI).
    :param update_user_password: UpdateUserPassword model including the current and the new password.
    """
    await auth_service.update_user_password(request, update_user_password)
