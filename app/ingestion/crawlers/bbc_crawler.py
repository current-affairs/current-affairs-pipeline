from bs4 import BeautifulSoup
from datetime import datetime
import re

from app.ingestion.crawlers.base_crawler import BaseCrawler
from app.ingestion.crawlers.crawler_utils import clean_text, remove_boilerplate
from app.schemas.digest.item import DigestItem

class BbcCrawler(BaseCrawler):
    
    def parse(self, html: str, item: DigestItem) -> dict:
        soup = BeautifulSoup(html, "lxml")

        article = soup.find("article")
        if not article:
            return {}

        paragraphs = []

        blocks = article.find_all("div", attrs={"data-component": "text-block"})

        for block in blocks:
            for p in block.find_all("p"):
                text = clean_text(p.get_text(" ", strip=True))

                # Filter junk
                if not text or len(text.split()) < 8:
                    continue

                if "Follow BBC" in text:
                    continue

                paragraphs.append(text)

        content = "\n\n".join(dict.fromkeys(paragraphs))

        # Title
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else item.title

        # Published date
        time_tag = soup.find("time")
        published = time_tag.get("datetime") if time_tag else item.published_at

        return {
            "title": title,
            "content": content,
            "published_at": published
        }
        
    def clean(self, data: dict) -> DigestItem:
        content = clean_text(data["content"])
        return content


# Backward-compatible alias.
BBCCrawler = BbcCrawler