import logging
from app.schemas.ingestion.request import IngestRequest
from app.workers.rss_ingestion_worker import process_rss_feed_content

async def ingest_rss(data: IngestRequest) -> dict:
    """
        Ingest RSS feed
    """
    try:
        process_rss_feed_content(data.model_dump())
        
        return {
            "status": "saved",
            "message": f"Successfully processed {data.name}",
            "feed_name": data.name,
            "url": data.url
        }
    except Exception as e:
        logging.error(f"Error in ingest_rss: {str(e)}")
        raise