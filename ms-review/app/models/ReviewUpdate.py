from pydantic import BaseModel
from typing import Optional


class ReviewUpdate(BaseModel):
    username: Optional[str] = None
    image: Optional[str] = None
