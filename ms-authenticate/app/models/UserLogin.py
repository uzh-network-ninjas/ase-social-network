from typing import Optional
from pydantic import BaseModel


class UserLogin(BaseModel):
    id: Optional[str] = None
    username: str | None = None
    email: str | None = None
    password: str

    @staticmethod
    def check_username_or_email(values):
        username, email = values.get('username'), values.get('email')
        if not (username or email):
            raise ValueError('Either username or email must be provided.')
        return values
