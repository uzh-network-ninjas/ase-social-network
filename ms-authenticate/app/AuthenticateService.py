from app.AuthenticateRepository import AuthenticateRepository
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.models.UserRegisterIn import UserRegisterIn
from app.models.UserLoginIn import UserLoginIn
from datetime import timedelta, datetime
import jwt


class AuthenticateService:
    def __init__(self):
        self.auth_repo = AuthenticateRepository()
        self.auth_encryption = {
            'SECRET_KEY': 'H8WBDhQlcfjoFmIiYymmkRm1y0A2c5WU',
            'ALGORITHM': 'HS256',
            'ACCESS_TOKEN_EXPIRE_MINUTES': 300,
            'KID': 'ooNKWeo0vijweijrKn234123J93c0qkD',
            'pwd_context': CryptContext(schemes=["bcrypt"], deprecated="auto"),
            'oauth2_scheme': OAuth2PasswordBearer(tokenUrl="token")
        }

    def generate_token(self, user):
        access_token_expires = timedelta(minutes=self.auth_encryption['ACCESS_TOKEN_EXPIRE_MINUTES'])
        to_encode = {'sub': user.username}.copy()
        expire = datetime.now() + (access_token_expires or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self.auth_encryption['SECRET_KEY'],
            algorithm=self.auth_encryption['ALGORITHM'],
            headers={"kid": self.auth_encryption['KID']}
        )

    async def register_user(self, user: UserRegisterIn):
        if await self.auth_repo.find_user_by_name(user.username):
            raise HTTPException(status_code=409, detail="Username already exists")
        if await self.auth_repo.find_user_by_email(user.email):
            raise HTTPException(status_code=409, detail="Email already in use")
        hashed_password = self.auth_encryption['pwd_context'].hash(user.password)
        user.password = hashed_password
        return await self.auth_repo.add_user(user)

    async def login_user(self, user: UserLoginIn):
        if not await self.auth_repo.find_user(user):
            raise HTTPException(status_code=404, detail="User not found")
        hashed_user = await self.auth_repo.get_user(user)
        if not self.auth_encryption['pwd_context'].verify(user.password, hashed_user.password):
            raise HTTPException(status_code=404, detail="Invalid password")
        return self.generate_token(user)
