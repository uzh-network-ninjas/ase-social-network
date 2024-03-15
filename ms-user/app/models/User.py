from pydantic import BaseModel
from typing import List, Optional

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    preferences: Optional[List[str]] = []

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    preferences: Optional[List[str]] = None