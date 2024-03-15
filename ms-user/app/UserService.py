from fastapi import HTTPException
from app.models.User import UserOut, UserUpdate
from app.UserRepository import UserRepository

class UserService:
    def __init__(self):
        self.ur = UserRepository()

    async def get_user_by_id(self, user_id: str):
        result = await self.ur.find_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    async def get_user_by_username(self, username: str):
        result = await self.ur.find_by_username(username)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        result["id"] = str(result["_id"])
        return UserOut(**result)

    async def update_user_by_id(self, user_id: str, updated_user: UserUpdate):
        result = await self.ur.update_user(user_id, updated_user)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        updated_user["id"] = user_id
        return UserOut(**updated_user)

    async def delete_user_by_id(self, user_id):
        result = await self.ur.delete_user_by_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found!")
        return {"deleted": result["username"]}