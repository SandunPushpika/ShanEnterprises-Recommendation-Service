from pydantic import BaseModel #type: ignore
from typing import List, Dict

class ReviewRequest(BaseModel):
    vehicle_id: int

class RankRequest(BaseModel):
    query: str
    limit: int = 5