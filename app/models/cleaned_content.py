from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, UUID
import uuid
from datetime import datetime
from app.core.database import Base

class CleanedContent(Base):
    __tablename__ = "cleaned_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_name = Column(String)
    source_url = Column(String, unique=True)
    title = Column(Text)
    content = Column(Text)

    published_at = Column(DateTime)

    language = Column(String, default="en")
    
    status = Column(Integer, default=0)