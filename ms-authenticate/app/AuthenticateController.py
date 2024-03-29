from fastapi import FastAPI, status, Request
from app.AuthenticateService import AuthenticateService
from app.models.UserLogin import UserLogin
from app.models.UserRegister import UserRegister
from app.models.UpdateUserPassword import UpdateUserPassword

app = FastAPI()
auth_service = AuthenticateService()


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister) -> dict:
    registered_user = await auth_service.register_user(user)
    access_token = await auth_service.login_user(registered_user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token", status_code=status.HTTP_201_CREATED)
async def login_generate_token(user: UserLogin) -> dict:
    access_token = await auth_service.login_user(user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(request: Request, update_user_password: UpdateUserPassword):
    await auth_service.update_user_password(request, update_user_password)
