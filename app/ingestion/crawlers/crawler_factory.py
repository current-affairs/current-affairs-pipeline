from app.ingestion.crawlers.bbc_crawler import BbcCrawler
from app.ingestion.crawlers.hindu_crawler import HinduCrawler
from app.ingestion.crawlers.pib_crawler import PibCrawler


class CrawlerFactory:

    @staticmethod
    def get_crawler(source: str):
        source = source.lower()

        if source == "pib":
            return PibCrawler()

        if source == "the hindu":
            return HinduCrawler()

        if source == "bbc india":
            return BbcCrawler()

        raise ValueError(f"No crawler for source: {source}")