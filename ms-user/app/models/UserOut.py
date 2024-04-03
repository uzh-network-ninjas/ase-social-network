from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    image: Optional[str] = None
    preferences: Optional[List[str]] = []
    restrictions: Optional[List[str]] = []
    following: Optional[List[str]] = []
    followers: Optional[List[str]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None