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
        """Initializes the AuthenticateService with a AuthenticateRepository instance
        and the required jwt information used for token handling and hashing.
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
        """Creates a new token.

        :param user: The user data (UserLogin model).
        :return: The created access token including user_id, user_name and expires_at.
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
        """Extracts the user ID from the request.

        :param request: The request object.
        :return: The user ID.
        """
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload["sub"]

    async def register_user(self, user: UserRegister) -> UserLogin:
        """Registers a new user.

        :param user: The user data (UserRegister model).
        :return: The registered user.
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
        if not await self.auth_repo.user_exists(user):
            raise HTTPException(status_code=404, detail="User not found")
        hashed_user = await self.auth_repo.get_user_by_name_or_email(user)
        if not self.auth_encryption['pwd_context'].verify(user.password, hashed_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        return self.generate_token(hashed_user)

    async def update_user_password(self, request: Request, update_user_password: UpdateUserPassword):
        hashed_user = await self.auth_repo.get_user_by_id(self.extract_user_id(request))
        if not self.auth_encryption['pwd_context'].verify(update_user_password.curr_password, hashed_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        if update_user_password.curr_password == update_user_password.new_password:
            raise HTTPException(status_code=400, detail="The new password must differ from the current one")
        await self.auth_repo.update_user_password(hashed_user.id, self.auth_encryption['pwd_context'].hash(update_user_password.new_password))
