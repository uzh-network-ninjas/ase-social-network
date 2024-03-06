from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# FastAPI app
app = FastAPI()

# User Crud - EDIT, DELETE, GET (no create we create only via register, all other values like images are via update only)

@app.get("/helloworld")
def read_root():
    return {"Hello": "World"}