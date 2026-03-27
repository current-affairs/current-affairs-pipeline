
from typing import List, Optional
from pydantic import BaseModel

from app.core.feed_status import FeedStatus


class DigestRequest(BaseModel):
    languages: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    limit: Optional[int] = None
    status: Optional[FeedStatus] = FeedStatus.Pending