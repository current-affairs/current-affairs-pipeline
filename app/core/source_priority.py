SOURCE_PRIORITY = {
    "PIB": 10,
    "PRS": 9,
    "The Hindu": 8,
    "Indian Express": 8,
    "Business Standard": 7,
    "BBC India": 6,
    "Guardian India": 6,
    "Dainik Bhaskar": 5
}


def get_source_priority(source_name: str) -> int:
    return SOURCE_PRIORITY.get(source_name, 5)