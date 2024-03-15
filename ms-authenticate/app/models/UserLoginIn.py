from typing import Optional
from pydantic import BaseModel

class UserLoginIn(BaseModel):
    id: Optional[str] = None
    username: str | None = None
    email: str | None = None
    password: str

    def check_username_or_email(self, values):
        username, email = values.get('username'), values.get('email')
        if not (username or email):
            raise ValueError('Either username or email must be provided.')
        return values
