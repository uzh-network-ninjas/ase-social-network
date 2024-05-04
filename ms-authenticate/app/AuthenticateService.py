from app.AuthenticateRepository import AuthenticateRepository
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.models.UserRegister import UserRegister
from app.models.UserLogin import UserLogin
from app.models.UpdateUserPassword import UpdateUserPassword
from datetime import timedelta, datetime
import jwt
import os


class AuthenticateService:
    def __init__(self):
        """
        Initializes the AuthenticateService with a AuthenticateRepository instance
        and the required configuration for handling authentication,
        including JWT token generation and password hashing.
        """
        self.auth_repo = AuthenticateRepository()
        self.auth_encryption = {
            'SECRET_KEY': os.getenv("JWT_SECRET", "no_key"),
            'ALGORITHM': os.getenv("JWT_ALGORITHM", "HS256"),
            'ACCESS_TOKEN_EXPIRE_MINUTES': os.getenv("JWT_EXPIRE_MINUTES", 3000),
            'KID': os.getenv("JWT_KONG_KEY", "no_key"),
            'pwd_context': CryptContext(schemes=["bcrypt"], deprecated="auto"),
            'oauth2_scheme': OAuth2PasswordBearer(tokenUrl="token")
        }

    def generate_token(self, user: UserLogin) -> str:
        """
        Generates a JWT token.

        :param user: The user object containing the user's credentials (UserLogin model).
        :return: The created JWT token.
        """
        access_token_expires = timedelta(minutes=self.auth_encryption['ACCESS_TOKEN_EXPIRE_MINUTES'])
        to_encode = {'sub': user.id, 'username': user.username}
        expire = datetime.now() + (access_token_expires or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self.auth_encryption['SECRET_KEY'],
            algorithm=self.auth_encryption['ALGORITHM'],
            headers={"kid": self.auth_encryption['KID']}
        )

    @staticmethod
    def extract_user_id(request: Request) -> str:
        """
        Extracts the user ID from the authorization token provided in the request headers.

        :param request: The request object that includes the Authorization header (provided by FastAPI).
        :return: The user ID from the decoded JWT token.
        """
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload["sub"]

    async def register_user(self, user: UserRegister) -> UserLogin:
        """
        Registers a new user and returns the user's login credentials if successful.

        :param user: The user registration data (UserRegister model).
        :return: The registered user's login information.
        :raises HTTPException(409): If the username or email is already in use.
        """
        if await self.auth_repo.username_exists(user.username):
            raise HTTPException(status_code=409, detail="Username already exists")
        if await self.auth_repo.user_email_exists(user.email):
            raise HTTPException(status_code=409, detail="Email already in use")
        user_to_register = user.copy()
        user_to_register.password = self.auth_encryption['pwd_context'].hash(user.password)
        registered_user = await self.auth_repo.add_user(user_to_register)
        registered_user.password = user.password
        return registered_user

    async def login_user(self, user: UserLogin) -> str:
        """
        Authenticates a user's login credentials and returns a JWT token if successful.

        :param user: The user login data (UserLogin model).
        :return: The created JWT token.
        :raises HTTPException(404): If the user is not found
        :raises HTTPException(401): If the password is invalid.
        """
        if not await self.auth_repo.user_exists(user):
            raise HTTPException(status_code=404, detail="User not found")
        hashed_user = await self.auth_repo.get_user_by_name_or_email(user)
        if not self.auth_encryption['pwd_context'].verify(user.password, hashed_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        return self.generate_token(hashed_user)

    async def update_user_password(self, request: Request, update_user_password: UpdateUserPassword):
        """
        Updates the password for an authenticated user.

        :param request: The request object containing the current user's token.
        :param update_user_password: Contains the current and new password.
        :raises HTTPException(401): If the current password is invalid.
        :raises HTTPException(400): If the new password is the same as the current one.
        """
        hashed_user = await self.auth_repo.get_user_by_id(self.extract_user_id(request))
        if not self.auth_encryption['pwd_context'].verify(update_user_password.curr_password, hashed_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        if update_user_password.curr_password == update_user_password.new_password:
            raise HTTPException(status_code=400, detail="The new password must differ from the current one")
        await self.auth_repo.update_user_password(hashed_user.id, self.auth_encryption['pwd_context'].hash(update_user_password.new_password))
