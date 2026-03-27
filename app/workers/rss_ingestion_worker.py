import feedparser
import logging
from app.services import feed_processing_service
from app.utils.date_utils import is_older_than_days, parse_rss_date
from app.utils.feed_entry_utils import debug_print_payload, extract_content, safe_get
from app.utils.url_utils import merge_feed_query_params

logging.basicConfig(level=logging.INFO)


# ============================
# 🔹 Main RSS Processor
# ============================
def process_rss_feed_content(feed_config):
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

            feed_processing_service.process_content(payload)

        except Exception as e:
            logging.error(
                f"Entry processing failed: {e} | source: {url}"
            )

    logging.info(f"Total processed: {feed_counter} | Source: {source}")


# Backward-compatible alias.
def process_rss_content(feed_config):
    return process_rss_feed_content(feed_config)