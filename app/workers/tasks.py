import feedparser
from dateutil import parser
from datetime import datetime
import logging
from services import feeds

logging.basicConfig(level=logging.INFO)

def parse_rss_date(date_string):
    if not date_string:
        return datetime.utcnow().isoformat()

    try:
        return parser.parse(date_string).isoformat()
    except Exception:
        return datetime.utcnow().isoformat()


def extract_content(entry):
    """
    Handles different RSS formats safely
    """
    if hasattr(entry, "summary"):
        return entry.summary

    if hasattr(entry, "content"):
        return entry.content[0].value

    return ""


def safe_get(entry, field, default=""):
    return getattr(entry, field, default)


def is_older_than_days(date_string, days=3):
    """
    Check if the given date is older than specified days
    """
    if not date_string:
        return False
    
    try:
        parsed_date = parser.parse(date_string)
        # Make parsed_date timezone-aware if it's naive
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=None)
            current_date = datetime.utcnow()
        else:
            current_date = datetime.now(parsed_date.tzinfo)
        
        age = current_date - parsed_date
        return age.days > days
    except Exception:
        # If date parsing fails, assume it's not older to be safe
        return False


def debug_print_payload(payload):
    print("\n Payload:")
    print(f"  Source: {payload['source_name']}")
    print(f"  Title: {payload['title'][:60]}")
    print(f"  Lang: {payload.get('language')}")
    print(f"  Date: {payload['published_at']}")
    print(f"  Content length: {len(payload['content'])}")


def process_rss_content(feed_config):
    source = feed_config["name"]
    url = feed_config["url"]
    language = feed_config.get("language")

    logging.info(f"Fetching: {source}")

    feed = feedparser.parse(url)

    if feed.bozo:
        logging.warning(f" Feed error: {source}")
        return
    feed_counter = 0
    for entry in feed.entries:
        feed_counter = feed_counter + 1
        try:
            title = safe_get(entry, "title")
            link = safe_get(entry, "link")
            published_date = safe_get(entry, "published", None)

            # Skip entries older than 3 days
            if is_older_than_days(published_date, days=3):
                logging.info(f"Skipping entry from {source}: '{title[:30]}' - older than 3 days")
                continue

            content = extract_content(entry)

            if not title or not content:
                continue

            payload = {
                "source_name": source,
                "source_type": "rss",
                "url": link,
                "title": title.strip(),
                "content": content.strip(),
                "published_at": parse_rss_date(published_date),
                "language": language
            }

            debug_print_payload(payload)
            feeds.process_content(payload)
            

        except Exception as e:
            logging.error(f"Entry processing failed: {e} for source: {url}")
    
    logging.info(f"Total feed: {feed_counter} for Source: {source}")