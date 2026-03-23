from datetime import datetime, timezone
from app.core.feed_status import FeedStatus
from app.schemas.digest_request import DigestRequest
from app.schemas.digest_item import DigestItem
from app.schemas.digest_response import DigestResponse
from app.core.database import get_db
from app.models.content import Content


def get_today_digest(request: DigestRequest):
    with get_db() as db:
        now_utc = datetime.now(timezone.utc)
        today_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)

        query = db.query(Content).filter(
            Content.is_canonical == True,
            Content.published_at >= today_start,
            Content.status == FeedStatus.Pending.value
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
                    id=str(content.id),
                    cluster_id=str(content.cluster_id),
                    title=content.title,
                    source=content.source_name,
                    published_at=content.published_at,
                    language=content.language,
                    content=content.content
                )
            )

        return DigestResponse(date=today_start.date().isoformat(), digest=digest_items)