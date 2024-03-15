from fastapi import FastAPI, status
from app.AuthenticateService import AuthenticateService
from app.models.UserIn import UserIn
from app.models.UserOut import UserOut

app = FastAPI()
auth_service = AuthenticateService()


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register(user: UserIn):
    return await auth_service.register_user(user)


@app.post("/token", status_code=status.HTTP_200_OK)
async def login_generate_token(user: UserIn):
    access_token = await auth_service.login_user(user)
    return {"access_token": access_token, "token_type": "bearer"}
