from app.ingestion.crawlers.bbc import BBCCrawler
from app.ingestion.crawlers.hindu import HinduCrawler
from app.ingestion.crawlers.pib import PIBCrawler


class CrawlerFactory:

    @staticmethod
    def get_crawler(source: str):
        source = source.lower()

        if source == "pib":
            return PIBCrawler()

        if source == "the hindu":
            return HinduCrawler()

        if source == "bbc india":
            return BBCCrawler()

        raise ValueError(f"No crawler for source: {source}")