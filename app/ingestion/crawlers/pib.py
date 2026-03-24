from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict

from app.ingestion.crawlers.base import BaseCrawler
from app.ingestion.crawlers.utils import clean_text, remove_boilerplate
from app.schemas.digest_item import DigestItem


class PIBCrawler(BaseCrawler):

    def parse(self, html: str, item: DigestItem) -> dict:
        soup = BeautifulSoup(html, "lxml")

        container = soup.select_one(
            "div.innner-page-main-about-us-content-right-part"
        )

        if not container:
            raise ValueError("PIB layout changed: main container not found")

        # ------------------------
        # Title
        # ------------------------
        title_tag = container.select_one("#Titleh2")
        title = title_tag.get_text(strip=True) if title_tag else item.title

        # ------------------------
        # Published Date
        # ------------------------
        published_at = item.published_at
        date_tag = container.select_one("#PrDateTime")

        if date_tag:
            raw = date_tag.get_text(" ", strip=True)

            match = re.search(r"(\d{1,2} \w+ \d{4}.*)", raw)
            if match:
                try:
                    published_at = datetime.strptime(
                        match.group(1), "%d %b %Y %I:%M%p"
                    )
                except Exception:
                    pass  # fallback to existing

        # ------------------------
        # Remove noise before extraction
        # ------------------------
        for tag in container.find_all(["script", "style", "iframe", "img", "video"]):
            tag.decompose()

        # ------------------------
        # Extract Paragraph Content
        # ------------------------
        content_parts: List[str] = []

        for tag in container.find_all(["p", "li"]):
            text = tag.get_text(" ", strip=True)

            if not text:
                continue

            if "Visitor Counter" in text:
                continue

            if "*****" in text:
                continue

            content_parts.append(text)

        # ------------------------
        # Extract Tables (Structured + Text)
        # ------------------------
        tables: List[List[Dict[str, str]]] = []
        table_texts: List[str] = []

        for table in container.select("table"):
            headers = []
            rows = []

            for i, tr in enumerate(table.select("tr")):
                cols = [td.get_text(" ", strip=True) for td in tr.select("td")]

                if not cols:
                    continue

                if i == 0:
                    headers = cols
                else:
                    if headers and len(cols) == len(headers):
                        rows.append(dict(zip(headers, cols)))

            if rows:
                tables.append(rows)

                # Convert table → readable sentences (LLM-friendly)
                table_sentences = self._format_table_as_sentences(rows)
                table_texts.append(table_sentences)

        # ------------------------
        # Combine Content
        # ------------------------
        content = "\n\n".join(content_parts)

        if table_texts:
            content += "\n\n---\n\nTable Data:\n\n"
            content += "\n\n".join(table_texts)

        return {
            "title": title,
            "published_at": published_at,
            "content": content,
        }

    # ------------------------
    # Convert table → LLM friendly sentences
    # ------------------------
    def _format_table_as_sentences(self, rows: List[Dict[str, str]]) -> str:
        sentences = []

        for row in rows:
            parts = [f"{key} is {value}" for key, value in row.items()]
            sentence = ", ".join(parts)
            sentences.append(sentence)

        return ". ".join(sentences)

    # ------------------------
    # Final Cleaning
    # ------------------------
    def clean(self, data: dict) -> DigestItem:
        content = clean_text(data["content"])
        content = remove_boilerplate(content)

        return DigestItem(
            id="",  # keep original or generate from URL
            cluster_id="",
            title=data["title"],
            source="PIB",
            published_at=data["published_at"],
            language="en",
            content=content
        )