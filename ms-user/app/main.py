from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client.ms_user_db
collection = db.user_collection


# FastAPI app
app = FastAPI()

# User Crud - EDIT, DELETE, GET (no create we create only via register, all other values like images are via update only)

@app.get("/helloworld")
def read_root():
    return {"Hello": "World"}