import json
import azure.functions as func
from app.services.ingest_service import ingest_rss
from app.schemas.digest.item import DigestItem
from app.schemas.digest.request import DigestRequest
from app.schemas.digest.response import DigestResponse
from app.schemas.ingestion.request import IngestRequest
from app.services.crawl_service import scrape_content
from app.services.digest_service import get_today_digest, clean_daily_digest

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="rss/ingest")
async def process_rss(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    ingest_request = IngestRequest(**req_body)
    response = await ingest_rss(ingest_request)
    return func.HttpResponse(json.dumps(response))

@app.route(route="digest/raw")
async def get_raw_digest(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    request = DigestRequest(**req_body)
    response = get_today_digest(request)

    return func.HttpResponse(
        response.model_dump_json(),
        mimetype="application/json"
    )

@app.route(route="digest/raw/clean")
async def clean_raw_digest(req: func.HttpRequest) -> func.HttpResponse:
    response = await clean_daily_digest()
    return func.HttpResponse(
        response.model_dump_json(),
        mimetype="application/json"
    )
    
@app.route(route="digest/crawl")
async def crawl_digest(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    request = DigestItem(**req_body)
    response = await scrape_content(request)
    return func.HttpResponse(
        response.model_dump_json(),
        mimetype="application/json"
    )