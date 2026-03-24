from abc import ABC, abstractmethod

from app.schemas.digest_item import DigestItem


class BaseCrawler(ABC):

    def crawl(self, item: DigestItem) -> DigestItem:
        html = self.fetch(item)
        parsed = self.parse(html, item)
        cleaned = self.clean(parsed)
        parsed["content"] = cleaned
        return parsed

    def fetch(self, item: DigestItem) -> str:
        import httpx

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = httpx.get(item.source_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text

    @abstractmethod
    def parse(self, html: str, item: DigestItem) -> dict:
        pass

    @abstractmethod
    def clean(self, data: dict) -> DigestItem:
        pass