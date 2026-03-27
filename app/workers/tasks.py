import feedparser
from dateutil import parser
from datetime import datetime, timezone
import logging
from app.services import feeds_service
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

logging.basicConfig(level=logging.INFO)


def merge_feed_query_params(entry_url: str, feed_url: str) -> str:
    """
    - Forces www for PIB
    - Appends query params from feed_url into entry_url
    - Avoids duplicates
    """
    if "pib.gov.in" not in entry_url:
        return entry_url

    entry_parsed = urlparse(entry_url)
    feed_parsed = urlparse(feed_url)

    # Force www
    netloc = "www.pib.gov.in"

    # Parse query params
    entry_qs = parse_qs(entry_parsed.query)
    feed_qs = parse_qs(feed_parsed.query)

    # Merge feed params into entry params (without overwriting existing like PRID)
    for key, value in feed_qs.items():
        if key not in entry_qs:
            entry_qs[key] = value

    # Rebuild query string
    new_query = urlencode(entry_qs, doseq=True)

    return urlunparse(entry_parsed._replace(netloc=netloc, query=new_query))

# ============================
# 🔹 Parse RSS Date (FIXED)
# ============================
def parse_rss_date(date_string):
    """
    Always return timezone-aware datetime
    """
    if not date_string:
        return datetime.now(timezone.utc)

    try:
        dt = parser.parse(date_string)

        # Ensure timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt

    except Exception:
        return datetime.now(timezone.utc)


# ============================
# 🔹 Extract Content Safely
# ============================
def extract_content(entry):
    if hasattr(entry, "summary"):
        return entry.summary

    if hasattr(entry, "content") and entry.content:
        return entry.content[0].value

    return ""


# ============================
# 🔹 Safe Getter
# ============================
def safe_get(entry, field, default=None):
    return getattr(entry, field, default)


# ============================
# 🔹 Filter Old Entries (FIXED)
# ============================
def is_older_than_days(date_string, days=3):
    if not date_string:
        return False

    try:
        parsed_date = parser.parse(date_string)

        # Normalize to UTC
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)

        current_date = datetime.now(timezone.utc)

        age = current_date - parsed_date
        return age.days > days

    except Exception:
        return False


# ============================
# 🔹 Debug Helper
# ============================
def debug_print_payload(payload):
    print("\n Payload:")
    print(f"  Source: {payload['source_name']}")
    print(f"  Title: {payload['title'][:60]}")
    print(f"  Date: {payload['published_at']}")
    print(f"  Content length: {len(payload['content'])}")


# ============================
# 🔹 Main RSS Processor
# ============================
def process_rss_content(feed_config):
    source = feed_config["name"]
    url = feed_config["url"]
    language = feed_config.get("language")

    logging.info(f"Fetching: {source}")

    feed = feedparser.parse(
        url,
        request_headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/rss+xml, application/xml;q=0.9,*/*;q=0.8",
        }
    )

    if feed.bozo:
        logging.warning(f"Feed parse warning: {feed.bozo_exception} with source: {source}")

    feed_counter = 0

    for entry in feed.entries:
        feed_counter += 1

        try:
            title = safe_get(entry, "title", "")
            link = safe_get(entry, "link", "")
            link = merge_feed_query_params(link, url)
            published_date = safe_get(entry, "published", None)

            # Skip old content early
            if is_older_than_days(published_date, days=3):
                print(
                    f"Skipping (old): {title[:40]}..."
                )
                continue

            content = extract_content(entry)

            if not title or not content:
                logging.info(f"No title or content for feed: {source}")

            payload = {
                "source_name": source,
                "source_type": "rss",
                "url": link,
                "title": title.strip(),
                "content": content.strip(),
                "published_at": parse_rss_date(published_date),
                "language": language,
            }

            debug_print_payload(payload)

            feeds_service.process_content(payload)

        except Exception as e:
            logging.error(
                f"Entry processing failed: {e} | source: {url}"
            )

    logging.info(f"Total processed: {feed_counter} | Source: {source}")