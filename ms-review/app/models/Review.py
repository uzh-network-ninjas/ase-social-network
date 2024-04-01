from pydantic import BaseModel

class ReviewCreateImage(BaseModel):
    image: str