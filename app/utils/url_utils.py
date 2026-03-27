from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


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
