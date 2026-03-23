from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, UUID
import uuid
from datetime import datetime
from app.core.database import Base

class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_name = Column(String)
    source_type = Column(String)
    source_url = Column(String, unique=True)

    title = Column(Text)
    content = Column(Text)

    published_at = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow())

    language = Column(String, default="en")
    cluster_id = Column(UUID(as_uuid=True), nullable=True)

    hash = Column(String, index=True)

    is_canonical = Column(Boolean, default=False)
    source_priority = Column(Integer, default=5)

    importance = Column(Integer, default=5)

    status = Column(Integer, default=0)