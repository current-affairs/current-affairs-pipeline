
from app.schemas.digest.item import DigestItem
from app.ingestion.crawlers.crawler_factory import CrawlerFactory
from app.services.cleaned_content_service import CleanedContentService

async def scrape_content(digest: DigestItem):
    crawler = CrawlerFactory.get_crawler(digest.source)
    enriched_item = crawler.crawl(digest)
    result = CleanedContentService().save_clean_content(digest, enriched_item)
    digest.content = result.content
    return digest