from bs4 import BeautifulSoup
from datetime import datetime

from app.ingestion.crawlers.base_crawler import BaseCrawler
from app.ingestion.crawlers.crawler_utils import clean_text
from app.schemas.digest.item import DigestItem


class HinduCrawler(BaseCrawler):

    def parse(self, html: str, item: DigestItem) -> dict:
        soup = BeautifulSoup(html, "lxml")

        # 🎯 MAIN CONTENT (MOST IMPORTANT)
        content_div = soup.select_one("#schemaDiv")

        if not content_div:
            raise ValueError("Hindu layout changed: schemaDiv not found")

        content_parts = []

        # ✅ Extract paragraphs + subheadings
        for tag in content_div.find_all(["p", "h4"]):

            # Skip ads or empty blocks
            if tag.find_parent(class_="article-ad"):
                continue

            text = tag.get_text(" ", strip=True)

            if not text:
                continue

            # Skip "Also Read"
            if "Also read" in text:
                continue

            content_parts.append(text)

        content = "\n\n".join(content_parts)

        # 📰 Title fallback
        title = item.title

        # 📅 Published date
        date_tag = soup.select_one(".publish-time-new span")
        published_at = item.published_at

        if date_tag:
            try:
                raw = date_tag.get_text(strip=True)
                published_at = datetime.strptime(
                    raw.replace("Published - ", "").strip(),
                    "%B %d, %Y %I:%M %p IST"
                )
            except:
                pass

        return {
            "title": title,
            "published_at": published_at,
            "content": content
        }

    def clean(self, data: dict) -> DigestItem:
        content = clean_text(data["content"])
        return content