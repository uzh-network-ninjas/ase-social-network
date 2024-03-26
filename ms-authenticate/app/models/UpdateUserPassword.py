from pydantic import BaseModel


class UpdateUserPassword(BaseModel):
    curr_password: str
    new_password: str
