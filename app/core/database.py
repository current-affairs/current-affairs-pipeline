from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from typing import Generator
from contextlib import contextmanager

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


@contextmanager
def get_db() -> Generator:
    """
    Context manager for database sessions.
    Ensures session is properly closed after use.
    
    Usage:
        with get_db() as db:
            # Use db session
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()