from sqlalchemy.orm import Session
from app.models.content import Content
from datetime import datetime, timezone

def compute_score(content) -> int:
    score = 0

    # ========================
    # 1. Source priority
    # ========================
    score += content.source_priority * 2

    # ========================
    # 2. Content length
    # ========================
    if content.content:
        length = len(content.content)
        if length > 1000:
            score += 3
        elif length > 500:
            score += 2
        else:
            score += 1

    # ========================
    # 3. Language preference
    # ========================
    if content.language == "en":
        score += 1

    # ========================
    # 4.  RECENCY BOOST
    # ========================
    if content.published_at:
        now = datetime.now(timezone.utc)

        # ensure timezone safe
        pub_time = content.published_at
        if pub_time.tzinfo is None:
            pub_time = pub_time.replace(tzinfo=timezone.utc)

        age_seconds = (now - pub_time).total_seconds()

        #  scoring buckets
        if age_seconds < 1800:        # < 30 min
            score += 5
        elif age_seconds < 3600:      # < 1 hour
            score += 4
        elif age_seconds < 3 * 3600:  # < 3 hours
            score += 3
        elif age_seconds < 6 * 3600:  # < 6 hours
            score += 2
        elif age_seconds < 12 * 3600: # < 12 hours
            score += 1
        else:
            score += 0

    return score


def update_canonical_for_cluster(db: Session, cluster_id):
    items = db.query(Content).filter(
        Content.cluster_id == cluster_id
    ).all()

    if not items:
        return

    best_item = max(items, key=compute_score)

    # reset all
    for item in items:
        item.is_canonical = False

    # set best
    best_item.is_canonical = True

    db.commit()