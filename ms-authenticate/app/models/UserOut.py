from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserOut(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None