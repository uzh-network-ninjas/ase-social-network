from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class UserRegisterIn(BaseModel):
    username: str
    email: str
    password: str
    preferences: List[str] = []
    restrictions: List[str] = []
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
