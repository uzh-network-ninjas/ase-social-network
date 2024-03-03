from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Comment(BaseModel):
    user_id: int
    content: str
    created_at: datetime = datetime.now()