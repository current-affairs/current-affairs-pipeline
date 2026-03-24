
from app.schemas.digest_item import DigestItem
from app.ingestion.crawlers.factory import CrawlerFactory
from app.services.content_service import ContentService

async def scrap_content(digest: DigestItem):
    crawler = CrawlerFactory.get_crawler(digest.source)
    enriched_item = crawler.crawl(digest)
    result = ContentService().save_clean_content(digest, enriched_item)
    digest.content = result.content
    return digest
  
    