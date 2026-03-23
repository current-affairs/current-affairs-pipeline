# app/api/ingest.py
import logging
from app.schemas.ingest import IngestRequest
from app.workers.tasks import process_rss_content

async def ingest_rss(data: dict) -> dict:
    """
        Ingest RSS feed
    """
    try:
        ingest_request = IngestRequest(**data)
        
        process_rss_content(ingest_request.model_dump())
        
        return {
            "status": "saved",
            "message": f"Successfully processed {ingest_request.name}",
            "feed_name": ingest_request.name,
            "url": ingest_request.url
        }
    except Exception as e:
        logging.error(f"Error in ingest_rss: {str(e)}")
        raise