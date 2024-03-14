from fastapi import FastAPI

from app.models.User import User
from app.UserRepository import UserRepository

app = FastAPI()
ur = UserRepository()

@app.patch("/")
async def read_root():
    user = User(username="jerome", email="jerome@chad.com", password="giga")
    result = await ur.add_user(user)

    return {"newly created user": result}

@app.get("/{user_id}")
async def get_user(user_id: str):
    result = await ur.get_user(user_id)

    return {"retrieved user": result}