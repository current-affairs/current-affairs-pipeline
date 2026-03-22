
from typing import List, Optional
from pydantic import BaseModel


class DigestRequest(BaseModel):
    languages: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    limit: Optional[int] = None 