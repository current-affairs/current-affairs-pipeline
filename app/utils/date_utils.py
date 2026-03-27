from datetime import datetime, timezone

from dateutil import parser


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
