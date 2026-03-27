def extract_content(entry):
    if hasattr(entry, "summary"):
        return entry.summary

    if hasattr(entry, "content") and entry.content:
        return entry.content[0].value

    return ""


def safe_get(entry, field, default=None):
    return getattr(entry, field, default)


def debug_print_payload(payload):
    print("\n Payload:")
    print(f"  Source: {payload['source_name']}")
    print(f"  Title: {payload['title'][:60]}")
    print(f"  Date: {payload['published_at']}")
    print(f"  Content length: {len(payload['content'])}")
