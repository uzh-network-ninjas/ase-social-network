from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None
    preferences: Optional[List[str]] = []
    restrictions: Optional[List[str]] = []
    following: Optional[List[str]] = []
    followers: Optional[List[str]] = []
    updated_at: Optional[datetime] = None
