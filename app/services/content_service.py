from app.core.database import get_db
from sqlalchemy import update
from app.core.feed_status import FeedStatus
from app.models.cleaned_content import CleanedContent
from app.models.content import Content
from app.schemas.digest_item import DigestItem
from app.services.language import detect_language
import logging

logger = logging.getLogger(__name__)


class ContentService():
    def save_clean_content(self, digest_item: DigestItem, crawl_item):
        summary = crawl_item["content"] if crawl_item["content"] else digest_item.content
        content = CleanedContent(
            source_name=digest_item.source,
            source_url=digest_item.source_url,
            title=crawl_item["title"] if crawl_item["title"] else digest_item.title,
            content=summary,
            published_at=digest_item.published_at,
            language=detect_language(summary),
            status=FeedStatus.Pending.value
        )
        try:
            with get_db() as db:
                db.add(content)
                db.execute(update(Content).where(Content.id == digest_item.id).values(
                    status=FeedStatus.Picked.value))
                db.commit()
        except Exception as ex:
            logger.error(
                f"Clean Database Add/update failed for {digest_item.id}: with error {ex}")

        return content
