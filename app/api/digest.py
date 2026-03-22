from datetime import datetime, timedelta, timezone
from schemas.digest_request import DigestRequest
from schemas.digest_item import DigestItem
from schemas.digest_response import DigestResponse
from core.database import SessionLocal
from models.content import Content


# ==========================
# ROUTE: /digest/today
# ==========================
def get_today_digest(request: DigestRequest):
    db = SessionLocal()

    now_utc = datetime.now(timezone.utc)
    today_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    query = db.query(Content).filter(
        Content.is_canonical == True,
        Content.published_at >= today_start,
        Content.published_at < today_end
    )

    if request.languages:
        query = query.filter(Content.language.in_(request.languages))
    
    if request.limit:
        query = query.order_by(Content.published_at.asc()).limit(request.limit)
    else:
        query = query.order_by(Content.published_at.asc())

    # Query canonical content only
    canonical_contents = query.all()

    digest_items = []
    for content in canonical_contents:
        digest_items.append(
            DigestItem(
                cluster_id=str(content.cluster_id),
                title=content.title,
                source=content.source_name,
                published_at=content.published_at,
                language=content.language,
                content=content.content,
                tags=[],
            )
        )

    return DigestResponse(date=today_start.date().isoformat(), digest=digest_items)