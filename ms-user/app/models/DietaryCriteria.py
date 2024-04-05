from app.models.Preferences import Preferences
from app.models.Restrictions import Restrictions
from pydantic import BaseModel
from typing import List


class DietaryCriteria(BaseModel):
    preferences: List[Preferences]
    restrictions: List[Restrictions]