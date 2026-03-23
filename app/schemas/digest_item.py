from datetime import datetime
from typing import List

from pydantic import BaseModel

class DigestItem(BaseModel):
    id: str
    cluster_id: str
    title: str
    source: str
    published_at: datetime
    language: str
    content: str