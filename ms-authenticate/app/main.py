from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Models
class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

# Security
# SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
SECRET_KEY = "H8WBDhQlcfjoFmIiYymmkRm1y0A2c5WU"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
KID = "ooNKWeo0vijweijrKn234123J93c0qkD"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock database
users_db = {
    # Example user
}

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    return db.get(username)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return UserInDB(**user)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM, headers={"kid": KID})
    return encoded_jwt

# This is a mock database of users
users_db = {
    "adam": {
        "username": "adam",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2a$12$5hucHCsV02gQAOF3FQMIPO/cGuRaxKuUe1SwypgWZgXs5/6fpcrA2", #adam
        "disabled": False,
    }
}



# FastAPI app
app = FastAPI()


#!! this one uses formDATA
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegistration):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "disabled": False
    }
    return {"message": "User registered successfully."}

@app.get("/helloworld")
def read_root():
    return {"Hello": "World"}