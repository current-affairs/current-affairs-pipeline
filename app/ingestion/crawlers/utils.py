import re

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_boilerplate(text: str) -> str:
    if "This information was provided by" in text:
        text = text.split("This information was provided by")[0]
    return text