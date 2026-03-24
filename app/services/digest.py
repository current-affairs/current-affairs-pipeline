from datetime import datetime, timezone
from venv import logger
from sqlalchemy import update
from app.core.feed_status import FeedStatus
from app.schemas.clean_digest_result import CleanDigestResult
from app.schemas.digest_request import DigestRequest
from app.schemas.digest_item import DigestItem
from app.schemas.digest_response import DigestResponse
from app.core.database import get_db
from app.models.content import Content
from app.services.azure_ai import filter_digest
import logging

logger = logging.getLogger(__name__)


def get_today_digest(request: DigestRequest) -> DigestResponse:
    with get_db() as db:
        now_utc = datetime.now(timezone.utc)
        today_start = now_utc.replace(
            hour=0, minute=0, second=0, microsecond=0)

        query = db.query(Content).filter(
            Content.is_canonical == True,
            Content.published_at >= today_start,
            Content.status == request.status.value
        )

        if request.languages:
            query = query.filter(Content.language.in_(request.languages))

        if request.limit:
            query = query.order_by(
                Content.published_at.asc()).limit(request.limit)
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


def map_status_to_enum(status_text: str) -> FeedStatus:
    """Map AI response to FeedStatus enum."""
    if status_text == "ReadyToTake":
        return FeedStatus.ReadyToTake
    elif status_text == "Ignore":
        return FeedStatus.Ignore
    else:
        return FeedStatus.Pending


async def clean_daily_digest() -> CleanDigestResult:
    digests = get_today_digest(DigestRequest())
    updates = []
    warnings = []
    errors = []

    for dg in digests.digest:
        try:
            status_text = await filter_digest(dg.title, dg.content)
            status = map_status_to_enum(status_text)

            if status_text not in ["ReadyToTake", "Ignore"]:
                warnings.append({
                                "id": dg.id,
                                "title": dg.title,
                                "message": f"Unexpected status '{status_text}', defaulted to Pending"
                                })

            updates.append((dg.id, status.value))
            print(f"Content {dg.id}: {status_text} -> {status.name}")
        except Exception as e:
            error_msg = f"Failed for id: {dg.id}, title: {dg.title}, error: {str(e)}"
            logger.error(error_msg)
            errors.append({
                "id": dg.id,
                "title": dg.title,
                "error": str(e)
            })
            updates.append((FeedStatus.Pending.value, dg.id))

    # Batch update
    db_success = True
    db_error = None

    if updates:
        with get_db() as db:
            try:
                for content_id, status_value in updates:
                    db.execute(
                        update(Content)
                        .where(Content.id == content_id)
                        .values(status=status_value)
                    )
            except Exception as e:
                db_success = False
                db_error = str(e)
                logger.error(f"Database update failed: {e}")
            
            db.commit()

    # Prepare result
    has_warnings = len(warnings) > 0
    has_errors = len(errors) > 0 or not db_success

    result = CleanDigestResult(
        status="failed" if (has_errors or has_warnings) else "success",
        total_processed=len(digests.digest),
        successful_updates=len(updates) - len(errors) if db_success else 0,
        failed_updates=len(errors) if db_success else len(digests.digest),
        warnings=warnings,
        errors=errors + ([{"database_error": db_error}] if db_error else [])
    )

    return result

