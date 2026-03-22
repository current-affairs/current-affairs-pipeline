from sqlalchemy.orm import Session
from models.content import Content

def is_duplicate(db: Session, hash_value: str):
    return db.query(Content).filter(Content.hash == hash_value).first()