from datetime import datetime
from pydantic import BaseModel


class UserRegisterIn(BaseModel):
    username: str
    email: str
    password: str
    created_at: datetime = datetime.now()
