import uuid
from sqlalchemy.orm import Session
from app.models.content import Content
from datetime import datetime, timedelta
from app.utils.text_similarity import simple_similarity

SIMILARITY_THRESHOLD = 0.75


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