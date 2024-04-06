from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    image: Optional[str] = None
    preferences: Optional[List[str]] = []
    restrictions: Optional[List[str]] = []
    following: Optional[List[str]] = []
    followers: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
