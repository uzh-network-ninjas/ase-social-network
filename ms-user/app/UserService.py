import jwt

from app.models.User import UserOut, UserUpdate
from app.UserRepository import UserRepository
from fastapi import HTTPException, Request

class UserService:
    def __init__(self):
        self.ur = UserRepository()

    async def get_user_by_id(self, user_id: str) -> UserOut:
        result = await self.ur.get_user_by_id(user_id)
        print(result)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    async def get_user_by_username(self, username: str) -> UserOut:
        result = await self.ur.get_user_by_username(username)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    #TODO currently still returns user
    async def update_user_by_id(self, user_id: str, updated_user: UserUpdate) -> UserUpdate:
        result = await self.ur.update_user_by_id(user_id, updated_user)
        if not result.raw_result["updatedExisting"]:
            raise HTTPException(status_code=400, detail="Could not update user!")
        return updated_user

    async def delete_user_by_id(self, user_id: str) -> dict[str, str]:
        result = await self.ur.delete_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        return {"deleted": result["username"]}

    @staticmethod
    def extract_user_id_from_token(request: Request) -> str:
        bearer = request.headers.get("Authorization")
        token = bearer.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["sub"]
        return user_id