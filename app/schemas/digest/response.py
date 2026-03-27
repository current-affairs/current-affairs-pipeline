from typing import List
from pydantic import BaseModel
from app.schemas.digest.item import DigestItem


class DigestResponse(BaseModel):
    date: str
    digest: List[DigestItem]