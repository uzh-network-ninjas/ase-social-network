import pprint
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from AuthenticateService import AuthenticateService
from models import User

app = FastAPI()
auth_service = AuthenticateService()


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User):
    result = await auth_service.register_user(user)
    # TODO: atm returning user w/ hashed password
    return {'registered user': result}


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: User):
    result = await auth_service.login_user(user)
    return {'logged in user': result}


# @app.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = auth_service.authenticate_user(users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = auth_service.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#
#     return {"access_token": access_token, "token_type": "bearer"}
#
# @app.post("/testuser")
# async def insert_user():
#     user = {"name": "test"}
#     result = await collection.insert_one(user)
#     pprint.pprint(result)
#     return {"result": "INSERTED"}
#
# @app.get("/testuser/{username}")
# async def find_user(username: str):
#     user = await collection.find_one({"name": username})
#     pprint.pprint(user)
#     return {"result": "RETURNED"}
#
# @app.get("/testuser")
# async def find_all_user():
#     users = collection.find()
#     pprint.pprint(users)
#     return {"result": "RETURNED ALL"}