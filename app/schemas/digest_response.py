from typing import List
from pydantic import BaseModel
from schemas.digest_item import DigestItem


class DigestResponse(BaseModel):
    date: str
    digest: List[DigestItem]