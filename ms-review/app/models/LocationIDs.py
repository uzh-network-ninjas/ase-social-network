from pydantic import BaseModel
from typing import List


class LocationIDs(BaseModel):
    location_ids: List[str]