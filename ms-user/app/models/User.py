from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    preferences: Optional[List[str]] = []
    restrictions: Optional[List[str]] = []
    updated_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    preferences: Optional[List[str]] = []
    restrictions: Optional[List[str]] = []
    updated_at: Optional[datetime] = None