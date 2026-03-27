import uuid
from sqlalchemy.orm import Session
from app.models.content import Content
from datetime import datetime, timedelta

SIMILARITY_THRESHOLD = 0.75

def simple_similarity(a: str, b: str) -> float:
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())

    if not a_words or not b_words:
        return 0.0

    return len(a_words & b_words) / len(a_words | b_words)


def find_cluster(db: Session, new_text: str):
    recent_items = db.query(Content).filter(
        Content.published_at > datetime.utcnow() - timedelta(days=2)
    ).all()

    for item in recent_items:
        sim = simple_similarity(new_text, item.content)

        if sim > SIMILARITY_THRESHOLD:
            return item.cluster_id or item.id  # fallback

    return None


def create_cluster():
    return uuid.uuid4()