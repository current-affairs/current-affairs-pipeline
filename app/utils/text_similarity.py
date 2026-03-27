def simple_similarity(a: str, b: str) -> float:
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())

    if not a_words or not b_words:
        return 0.0

    return len(a_words & b_words) / len(a_words | b_words)
