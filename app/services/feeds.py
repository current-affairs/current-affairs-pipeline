from app.core.database import get_db
from app.models.content import Content
from app.services.normalization import normalize_content
from app.services.dedup import is_duplicate
from app.services.cluster import find_cluster, create_cluster
from app.services.language import detect_language
from app.utils.hash import generate_hash
from app.services.canonical import update_canonical_for_cluster
from app.core.source_priority import get_source_priority
from app.core.feed_status import FeedStatus
import logging

logger = logging.getLogger(__name__)

def process_content(data):
    """
    Process content with automatic session management.
    The session is automatically closed after the with block.
    """
    with get_db() as db:
        try:

            # Clean and normalize content
            clean_text = normalize_content(data["content"])

            clean_text = clean_text if clean_text else data["title"]
            
            # Detect language
            language = detect_language(clean_text)
            
            # Generate hash for deduplication
            hash_value = generate_hash(clean_text)
            
            # Check for duplicates
            if is_duplicate(db, hash_value):
                logger.info(f"Duplicate content detected: {hash_value}")
                return "duplicate"
            
            # Find or create cluster
            cluster_id = find_cluster(db, clean_text)
            if not cluster_id:
                cluster_id = create_cluster()
            
            # Create content record
            content = Content(
                source_name=data["source_name"],
                source_type=data["source_type"],
                source_url=data["url"],
                title=data["title"],
                content=clean_text,
                language=language,
                published_at=data["published_at"],
                hash=hash_value,
                cluster_id=cluster_id,
                source_priority=get_source_priority(data["source_name"]),
                status = FeedStatus.Pending.value
            )
            
            # Save to database
            db.add(content)
            db.commit()
            print(f"Content stored successfully: {data['title']}")
            
            # Update canonical for cluster
            update_canonical_for_cluster(db, cluster_id)
            
            return "stored"
            
        except Exception as e:
            logger.error(f"Error processing content: {str(e)}")
            db.rollback()  # Rollback on error
            raise