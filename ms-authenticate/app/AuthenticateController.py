from fastapi import FastAPI, status, Request
from app.AuthenticateService import AuthenticateService
from app.models.UserLogin import UserLogin
from app.models.UserRegister import UserRegister
from app.models.UserOut import UserOut
from app.models.UpdateUserPassword import UpdateUserPassword

app = FastAPI()
auth_service = AuthenticateService()


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register(user: UserRegister) -> UserOut:
    return await auth_service.register_user(user)


@app.post("/token", status_code=status.HTTP_200_OK)
async def login_generate_token(user: UserLogin) -> dict:
    access_token = await auth_service.login_user(user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(request: Request, update_user_password: UpdateUserPassword):
    await auth_service.update_user_password(request, update_user_password)
