from pydantic import BaseModel
from datetime import datetime

class IngestRequest(BaseModel):
    name: str
    url: str
    url: str
    language: str
    priority: int