
from app.schemas.digest_item import DigestItem
from app.ingestion.crawlers.factory import CrawlerFactory

async def scrap_content(digest: DigestItem):
    crawler = CrawlerFactory.get_crawler(digest.source)
    enriched_item = crawler.crawl(digest)
    return enriched_item
  
    