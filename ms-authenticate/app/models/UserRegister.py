from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    image: Optional[str] = None
    preferences: List[str] = []
    restrictions: List[str] = []
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
