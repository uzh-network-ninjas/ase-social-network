from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .Comment import Comment

class Post(BaseModel):
    user_id: int  # ID of the user who created the post
    content: str  # The content of the post
    created_at: datetime = datetime.now()  # The timestamp when the post was created
    updated_at: Optional[datetime] = None  # The timestamp when the post was last updated, optional
    likes: int = 0  # Number of likes, default is 0
    comments: List[Comment] = []  # List of comments, starts empty
    tags: List[str] = []  # Optional tags for categorizing posts

    # Method to add a like to the post
    def add_like(self):
        self.likes += 1

    # Method to add a comment to the post
    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    # Method to update the post's content
    def update_content(self, new_content: str):
        self.content = new_content
        self.updated_at = datetime.now()