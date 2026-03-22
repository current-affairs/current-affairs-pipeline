from schemas.ingest import IngestRequest
from workers.tasks import process_rss_content

async def ingest_rss(data: IngestRequest):
    process_rss_content(data.model_dump())
    return {"status": "saved"}
    