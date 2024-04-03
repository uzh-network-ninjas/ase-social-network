from app.models.UserOut import UserOut
from pydantic import BaseModel
from typing import List


class UserListOut(BaseModel):
    users: List[UserOut]
