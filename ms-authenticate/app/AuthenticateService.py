from AuthenticateRepository import AuthenticateRepository
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from models.User import User


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

    def register_user(self, user: User):
        if await self.auth_repo.user_exists(user.id):
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = self.auth_encryption['pwd_context'].hash(user.password)
        # TODO: convert into HashedUser
        user.password = hashed_password
        return self.auth_repo.add_user(user)

    def login_user(self, user: User):
        if not await self.auth_repo.user_exists(user.id):
            raise HTTPException(status_code=404, detail="User not found")
        hashed_user = await self.auth_repo.get_user(user.id)
        if not self.auth_encryption['pwd_context'].verify(user.password, hashed_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        return user

    def delete_user(self, user: User):
        if not await self.auth_repo.user_exists(user.id):
            raise HTTPException(status_code=404, detail="User not found")
        self.auth_repo.delete_user(user.id)
        return {"status": "User deleted!"}




    # def verify_password(self, plain_password, hashed_password):
    #     return pwd_context.verify(plain_password, hashed_password)
    #
    # def get_user(self, db, username: str):
    #     return db.get(username)
    #
    # def authenticate_user(self, db, username: str, password: str):
    #     user = get_user(db, username)
    #     if not user or not verify_password(password, user["hashed_password"]):
    #         return False
    #     return UserInDB(**user)
    #
    # def create_access_token(self, data: dict, expires_delta: timedelta = None):
    #     to_encode = data.copy()
    #     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    #     to_encode.update({"exp": expire})
    #     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM, headers={"kid": KID})
    #     return encoded_jwt
